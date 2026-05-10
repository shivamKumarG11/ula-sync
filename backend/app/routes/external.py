from flask import Blueprint, g, request

from app.extensions import limiter
from app.services import external_service
from app.utils.helpers import make_response_envelope

external_bp = Blueprint("external", __name__, url_prefix="/api/v1/external")

_RATE = "30 per minute"


@external_bp.get("/cities/<city_slug>/weather")
@limiter.limit(_RATE)
def get_weather(city_slug):
    start = request.args.get("start", "")
    end = request.args.get("end", "")
    data = external_service.get_city_weather(city_slug, start, end)
    return make_response_envelope(data), 200


@external_bp.get("/cities/<city_slug>/pois")
@limiter.limit(_RATE)
def get_pois(city_slug):
    limit = min(request.args.get("limit", 20, type=int), 50)
    data = external_service.get_city_pois(city_slug, limit)
    return make_response_envelope(data), 200


@external_bp.get("/cities/<city_slug>/events")
@limiter.limit(_RATE)
def get_events(city_slug):
    start = request.args.get("start", "")
    end = request.args.get("end", "")
    data = external_service.get_city_events(city_slug, start, end)
    return make_response_envelope(data), 200


@external_bp.get("/cities/<city_slug>/air-quality")
@limiter.limit(_RATE)
def get_air_quality(city_slug):
    data = external_service.get_air_quality(city_slug)
    return make_response_envelope(data), 200


@external_bp.get("/cities/<city_slug>/wiki")
@limiter.limit(_RATE)
def get_wiki(city_slug):
    data = external_service.get_city_wiki(city_slug)
    return make_response_envelope(data), 200


@external_bp.get("/cities/<city_slug>/hotels")
@limiter.limit(_RATE)
def get_hotels(city_slug):
    checkin = request.args.get("check_in", "")
    checkout = request.args.get("check_out", "")
    data = external_service.get_hotels(city_slug, checkin, checkout)
    return make_response_envelope(data), 200


@external_bp.get("/cities/<city_slug>/restaurants")
@limiter.limit(_RATE)
def get_restaurants(city_slug):
    limit = min(request.args.get("limit", 5, type=int), 20)
    data = external_service.get_city_restaurants(city_slug, limit)
    return make_response_envelope(data), 200


@external_bp.get("/flights")
@limiter.limit(_RATE)
def get_flights():
    origin = request.args.get("origin", "")
    destination = request.args.get("destination", "")
    date = request.args.get("date", "")
    adults = request.args.get("adults", 1, type=int)
    data = external_service.get_flights(origin, destination, date, adults)
    return make_response_envelope(data), 200


@external_bp.get("/currency/rates")
@limiter.limit(_RATE)
def get_currency_rates():
    base = request.args.get("base", "USD")
    data = external_service.get_currency_rates(base)
    return make_response_envelope(data), 200


@external_bp.get("/countries/<code>/holidays/<int:year>")
@limiter.limit(_RATE)
def get_holidays(code, year):
    data = external_service.get_public_holidays(code.upper(), year)
    return make_response_envelope(data), 200


@external_bp.get("/countries/<name>")
@limiter.limit(_RATE)
def get_country(name):
    data = external_service.get_country_info(name)
    return make_response_envelope(data), 200
