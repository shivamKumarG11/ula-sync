"""
External API proxy service.

Design rules:
- Every public function returns safe data on failure (empty dict / empty list). Never raises.
- All HTTP calls have a 5-second timeout.
- Cache decorators use Flask-Caching with city-scoped keys.
- Amadeus access token is cached in the module-level dict _amadeus_token.
"""
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any

import requests

from app.extensions import cache
from app.models import City
from app.utils.errors import AppError

logger = logging.getLogger(__name__)

_TIMEOUT = 5  # seconds — external API hard limit

# Amadeus in-memory token cache
_amadeus_token: dict[str, Any] = {"access_token": None, "expires_at": 0}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get(url: str, *, params: dict | None = None, headers: dict | None = None) -> dict | list | None:
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        logger.warning("External GET failed url=%s: %s", url, exc)
        return None


def _city_or_404(slug: str) -> City:
    city = City.query.filter_by(slug=slug).first()
    if not city:
        raise AppError("City not found", 404)
    return city


# ---------------------------------------------------------------------------
# 1. Open-Meteo — Weather
# ---------------------------------------------------------------------------

def get_city_weather(city_slug: str, start: str, end: str) -> dict:
    cache_key = f"weather:{city_slug}:{start}:{end}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    city = _city_or_404(city_slug)
    if not city.latitude or not city.longitude:
        return {"error": "no_coordinates"}

    data = _get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": float(city.latitude),
            "longitude": float(city.longitude),
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode",
            "timezone": city.timezone or "auto",
            "start_date": start,
            "end_date": end,
        },
    )

    result = data if data else {}
    cache.set(cache_key, result, timeout=10800)  # 3 hours
    return result


# ---------------------------------------------------------------------------
# 2 & 3. Amadeus — Flights + Hotels
# ---------------------------------------------------------------------------

def _amadeus_token_get() -> str | None:
    now = time.time()
    if _amadeus_token["access_token"] and _amadeus_token["expires_at"] > now + 60:
        return _amadeus_token["access_token"]

    key = os.environ.get("AMADEUS_API_KEY", "")
    secret = os.environ.get("AMADEUS_API_SECRET", "")
    base = os.environ.get("AMADEUS_BASE_URL", "https://test.api.amadeus.com")

    try:
        resp = requests.post(
            f"{base}/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": key,
                "client_secret": secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=_TIMEOUT,
        )
        resp.raise_for_status()
        payload = resp.json()
        _amadeus_token["access_token"] = payload["access_token"]
        _amadeus_token["expires_at"] = now + payload.get("expires_in", 1800)
        return _amadeus_token["access_token"]
    except Exception as exc:
        logger.warning("Amadeus auth failed: %s", exc)
        return None


def get_flights(from_iata: str, to_iata: str, travel_date: str, adults: int = 1) -> dict:
    cache_key = f"flights:{from_iata}:{to_iata}:{travel_date}:{adults}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    token = _amadeus_token_get()
    if not token:
        return {"error": "amadeus_unavailable"}

    base = os.environ.get("AMADEUS_BASE_URL", "https://test.api.amadeus.com")
    data = _get(
        f"{base}/v2/shopping/flight-offers",
        params={
            "originLocationCode": from_iata,
            "destinationLocationCode": to_iata,
            "departureDate": travel_date,
            "adults": adults,
            "max": 5,
            "currencyCode": "USD",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    result = data if data else {"error": "no_data"}
    cache.set(cache_key, result, timeout=3600)  # 1 hour
    return result


def get_hotels(city_slug: str, checkin: str, checkout: str) -> dict:
    cache_key = f"hotels:{city_slug}:{checkin}:{checkout}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    city = _city_or_404(city_slug)
    iata = city.iata_code
    if not iata:
        return {"error": "no_iata_code"}

    token = _amadeus_token_get()
    if not token:
        return {"error": "amadeus_unavailable"}

    base = os.environ.get("AMADEUS_BASE_URL", "https://test.api.amadeus.com")
    headers = {"Authorization": f"Bearer {token}"}

    # Step 1: get hotel list by city
    hotels_list = _get(
        f"{base}/v1/reference-data/locations/hotels/by-city",
        params={"cityCode": iata, "radius": 5, "radiusUnit": "KM", "hotelSource": "ALL"},
        headers=headers,
    )

    if not hotels_list or "data" not in hotels_list:
        return {"error": "no_hotels"}

    hotel_ids = ",".join(h["hotelId"] for h in hotels_list["data"][:20])

    # Step 2: get offers
    offers = _get(
        f"{base}/v3/shopping/hotel-offers",
        params={
            "hotelIds": hotel_ids,
            "checkInDate": checkin,
            "checkOutDate": checkout,
            "adults": 1,
            "currency": "USD",
            "bestRateOnly": "true",
        },
        headers=headers,
    )

    result = offers if offers else {"error": "no_offers"}
    cache.set(cache_key, result, timeout=3600)
    return result


# ---------------------------------------------------------------------------
# 4. Frankfurter — Currency Rates
# ---------------------------------------------------------------------------

def get_currency_rates(base_currency: str = "USD") -> dict:
    cache_key = f"currency:{base_currency}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    data = _get(
        "https://api.frankfurter.app/latest",
        params={"from": base_currency, "to": "INR,EUR,GBP,JPY,AED,AUD,SGD"},
    )

    result = data if data else {}
    cache.set(cache_key, result, timeout=21600)  # 6 hours
    return result


# ---------------------------------------------------------------------------
# 6. RestCountries — Country Info
# ---------------------------------------------------------------------------

def get_country_info(country_name: str) -> dict:
    cache_key = f"country:{country_name.lower()}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    data = _get(
        f"https://restcountries.com/v3.1/name/{requests.utils.quote(country_name)}",
        params={"fields": "name,flags,currencies,languages,idd,capital,continents"},
    )

    result = data[0] if isinstance(data, list) and data else {}
    cache.set(cache_key, result, timeout=86400 * 30)  # 30 days
    return result


# ---------------------------------------------------------------------------
# 7. OpenTripMap — Points of Interest
# ---------------------------------------------------------------------------

def get_city_pois(city_slug: str, limit: int = 20) -> list:
    cache_key = f"pois:{city_slug}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    city = _city_or_404(city_slug)
    api_key = os.environ.get("OPENTRIPMAP_API_KEY", "")

    if not city.latitude or not city.longitude:
        return []

    data = _get(
        "https://api.opentripmap.com/0.1/en/places/radius",
        params={
            "radius": 10000,
            "lon": float(city.longitude),
            "lat": float(city.latitude),
            "kinds": "interesting_places,cultural,natural,religion",
            "rate": "2h",
            "format": "json",
            "limit": limit,
            "apikey": api_key,
        },
    )

    result = data if isinstance(data, list) else []
    cache.set(cache_key, result, timeout=86400)  # 24 hours
    return result


# ---------------------------------------------------------------------------
# 9. Ticketmaster — Events
# ---------------------------------------------------------------------------

def get_city_events(city_slug: str, start: str, end: str) -> dict:
    cache_key = f"events:{city_slug}:{start}:{end}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    city = _city_or_404(city_slug)
    api_key = os.environ.get("TICKETMASTER_API_KEY", "")

    data = _get(
        "https://app.ticketmaster.com/discovery/v2/events.json",
        params={
            "city": city.name,
            "countryCode": city.country_code or "",
            "startDateTime": f"{start}T00:00:00Z",
            "endDateTime": f"{end}T23:59:59Z",
            "size": 10,
            "sort": "date,asc",
            "apikey": api_key,
        },
    )

    result = data if data else {}
    cache.set(cache_key, result, timeout=7200)  # 2 hours
    return result


# ---------------------------------------------------------------------------
# 10. Nager.Date — Public Holidays
# ---------------------------------------------------------------------------

def get_public_holidays(country_code: str, year: int) -> list:
    cache_key = f"holidays:{country_code}:{year}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    data = _get(f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}")
    result = data if isinstance(data, list) else []
    cache.set(cache_key, result, timeout=86400)  # 24 hours
    return result


# ---------------------------------------------------------------------------
# 12. OpenAQ — Air Quality
# ---------------------------------------------------------------------------

def get_air_quality(city_slug: str) -> dict:
    cache_key = f"aqi:{city_slug}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    city = _city_or_404(city_slug)

    data = _get(
        "https://api.openaq.org/v2/latest",
        params={
            "city": city.name,
            "country": city.country_code or "",
            "parameter": "pm25",
            "limit": 1,
        },
    )

    result = data if data else {}
    cache.set(cache_key, result, timeout=1800)  # 30 minutes
    return result


# ---------------------------------------------------------------------------
# 13. Wikipedia — City Description
# ---------------------------------------------------------------------------

def get_city_wiki(city_slug: str) -> dict:
    cache_key = f"wiki:{city_slug}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    city = _city_or_404(city_slug)
    wiki_title = city.wikipedia_title or city.name

    data = _get(
        f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(wiki_title)}"
    )

    result = data if data else {}
    cache.set(cache_key, result, timeout=86400 * 7)  # 7 days
    return result


# ---------------------------------------------------------------------------
# 17. Yelp Fusion — Restaurants
# ---------------------------------------------------------------------------

def get_city_restaurants(city_slug: str, limit: int = 5) -> dict:
    cache_key = f"restaurants:{city_slug}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    city = _city_or_404(city_slug)
    api_key = os.environ.get("YELP_API_KEY", "")

    data = _get(
        "https://api.yelp.com/v3/businesses/search",
        params={
            "location": city.name,
            "categories": "restaurants",
            "sort_by": "rating",
            "limit": limit,
        },
        headers={"Authorization": f"Bearer {api_key}"},
    )

    result = data if data else {}
    cache.set(cache_key, result, timeout=7200)  # 2 hours
    return result
