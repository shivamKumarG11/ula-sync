import json
import logging
import math
import os
import re
from datetime import date

import requests

from app.extensions import db
from app.models import City, Stop, StopActivity, Trip, User
from app.models.enums import ExpenseTypeEnum
from app.prompts import (
    activity_suggestions,
    base_system,
    chatbot,
    itinerary_generation,
    packing_advice,
    transport_recommendation,
    trip_feedback,
)
from app.utils.errors import AppError

logger = logging.getLogger(__name__)

_TOKEN_ROUTER_BASE = os.environ.get("TOKEN_ROUTER_BASE_URL", "https://api.tokenrouter.com/v1")
_TOKEN_ROUTER_KEY = os.environ.get("TOKEN_ROUTER_API_KEY", "")

_FALLBACKS = {
    "generate-itinerary": (
        "AI itinerary generation is temporarily unavailable. "
        "You can still build your itinerary manually using the activity catalog."
    ),
    "suggest-activities": (
        "Activity suggestions are temporarily unavailable. "
        "Browse the catalog to find activities for your stop."
    ),
    "recommend-transport": (
        "Transport recommendations are temporarily unavailable. "
        "Check MakeMyTrip, IRCTC, or Skyscanner for options."
    ),
    "review-trip": (
        "Trip review is temporarily unavailable. "
        "You can still edit your itinerary in the builder."
    ),
    "packing-advice": (
        "Packing suggestions are temporarily unavailable. "
        "Use the default packing checklist as a starting point."
    ),
    "chat": "I'm having trouble responding right now. Please try again in a moment.",
}


# ---------------------------------------------------------------------------
# Core HTTP call
# ---------------------------------------------------------------------------

def _call_ai(
    messages: list[dict],
    model: str = "auto",
    temperature: float = 0.7,
    max_tokens: int = 1500,
) -> str:
    headers = {
        "Authorization": f"Bearer {_TOKEN_ROUTER_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    resp = requests.post(
        f"{_TOKEN_ROUTER_BASE}/chat/completions",
        json=payload,
        headers=headers,
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def _safe_call_ai(
    messages: list[dict],
    feature_key: str,
    model: str = "auto",
    temperature: float = 0.7,
    max_tokens: int = 1500,
) -> tuple[str, bool]:
    """Returns (content, is_fallback). Never raises."""
    try:
        content = _call_ai(messages, model=model, temperature=temperature, max_tokens=max_tokens)
        return content, False
    except requests.Timeout:
        logger.warning("AI timeout for feature=%s", feature_key)
    except requests.HTTPError as exc:
        logger.warning("AI HTTP error for feature=%s: %s", feature_key, exc)
    except Exception as exc:
        logger.exception("AI unexpected error for feature=%s: %s", feature_key, exc)

    return _FALLBACKS.get(feature_key, "AI is temporarily unavailable."), True


def _parse_json_response(text: str) -> dict | list | None:
    """Attempt to parse JSON from AI response, falling back to regex extraction."""
    text = text.strip()
    # Strip markdown code fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find the first JSON object or array
        match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
    return None


# ---------------------------------------------------------------------------
# Context loaders
# ---------------------------------------------------------------------------

def _load_trip_with_stops(trip_slug: str, user: User) -> Trip:
    trip = Trip.query.filter_by(slug=trip_slug, user_id=user.id).first()
    if not trip:
        raise AppError("Trip not found", 404)
    return trip


def _trip_stops_context(trip: Trip) -> list[dict]:
    stops = trip.stops.order_by(Stop.order_index).all()
    result = []
    for stop in stops:
        city = stop.city
        activities = [
            {
                "name": a.activity.name if a.activity else a.custom_name,
                "category": (a.category.value if hasattr(a.category, "value") else a.category),
                "cost_usd": float(a.custom_cost_usd or (a.activity.cost_usd if a.activity else 0) or 0),
                "duration_hours": float(a.duration_hours or (a.activity.duration_hours if a.activity else 1) or 1),
            }
            for a in stop.stop_activities.all()
        ]
        catalog = [
            {
                "name": act.name,
                "category": act.category.value if hasattr(act.category, "value") else act.category,
                "cost_usd": float(act.cost_usd or 0),
                "duration_hours": float(act.duration_hours or 1),
                "description": act.description or "",
            }
            for act in city.activities.limit(20).all()
        ]
        result.append(
            {
                "city": city.name,
                "country": city.country,
                "arrival_date": str(stop.arrival_date),
                "departure_date": str(stop.departure_date),
                "planned_activities": activities,
                "catalog_activities": catalog,
            }
        )
    return result


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _user_system_prompt(user: User, current_page: str | None = None, active_trip: Trip | None = None) -> str:
    interests = user.interests or []
    travel_style = user.travel_style.value if hasattr(user.travel_style, "value") else user.travel_style

    stop_count = None
    active_trip_name = None
    active_trip_start = None
    active_trip_end = None

    if active_trip:
        active_trip_name = active_trip.name
        active_trip_start = str(active_trip.start_date)
        active_trip_end = str(active_trip.end_date)
        stop_count = active_trip.stops.count()

    return base_system.build_system_with_context(
        username=user.username,
        preferred_currency=user.preferred_currency or "USD",
        home_city=user.home_city,
        home_country=user.home_country,
        travel_style=travel_style,
        interests=interests,
        active_trip_name=active_trip_name,
        active_trip_start=active_trip_start,
        active_trip_end=active_trip_end,
        stop_count=stop_count,
        current_page=current_page,
    )


# ---------------------------------------------------------------------------
# Feature: Generate Itinerary
# ---------------------------------------------------------------------------

def generate_itinerary(user: User, trip_slug: str, preferences: dict) -> dict:
    trip = _load_trip_with_stops(trip_slug, user)
    stops_data = _trip_stops_context(trip)

    start = trip.start_date
    end = trip.end_date
    total_days = (end - start).days + 1

    user_message = itinerary_generation.build_prompt(
        trip_name=trip.name,
        trip_start_date=str(start),
        trip_end_date=str(end),
        total_days=total_days,
        stops_data=stops_data,
        pace=preferences.get("pace", "moderate"),
        interests=preferences.get("interests"),
        budget_level=preferences.get("budget_level", "mid-range"),
        avoid=preferences.get("avoid"),
        preferred_currency=user.preferred_currency or "USD",
    )

    system = _user_system_prompt(user, active_trip=trip)
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]

    raw, is_fallback = _safe_call_ai(
        messages,
        feature_key="generate-itinerary",
        temperature=itinerary_generation.TEMPERATURE,
        max_tokens=itinerary_generation.MAX_TOKENS,
    )

    if is_fallback:
        return {"error": "ai_unavailable", "message": raw}

    parsed = _parse_json_response(raw)
    if parsed is None:
        return {"error": "parse_error", "message": raw}

    return parsed


# ---------------------------------------------------------------------------
# Feature: Suggest Activities
# ---------------------------------------------------------------------------

def suggest_activities(user: User, data: dict) -> dict:
    city = City.query.filter_by(slug=data["city_slug"]).first()
    if not city:
        raise AppError("City not found", 404)

    catalog = [
        {
            "name": act.name,
            "category": act.category.value if hasattr(act.category, "value") else act.category,
            "cost_usd": float(act.cost_usd or 0),
            "duration_hours": float(act.duration_hours or 1),
            "description": act.description or "",
        }
        for act in city.activities.limit(30).all()
    ]

    user_message = activity_suggestions.build_prompt(
        city_name=city.name,
        city_country=city.country,
        city_description=city.description or "",
        days_available=data.get("days_available", 2),
        budget_usd_per_day=data.get("budget_usd_per_day", 50),
        user_interests=data.get("user_interests", []),
        catalog_activities=catalog,
        existing_activity_names=data.get("existing_activity_ids", []),
    )

    system = _user_system_prompt(user)
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]

    raw, is_fallback = _safe_call_ai(
        messages,
        feature_key="suggest-activities",
        temperature=activity_suggestions.TEMPERATURE,
        max_tokens=activity_suggestions.MAX_TOKENS,
    )

    if is_fallback:
        return {"error": "ai_unavailable", "message": raw}

    parsed = _parse_json_response(raw)
    return parsed if parsed is not None else {"error": "parse_error", "message": raw}


# ---------------------------------------------------------------------------
# Feature: Recommend Transport
# ---------------------------------------------------------------------------

def recommend_transport(user: User, data: dict, flight_data: dict | None = None) -> dict:
    origin = City.query.filter_by(slug=data["origin_city_slug"]).first()
    destination = City.query.filter_by(slug=data["destination_city_slug"]).first()

    if not origin or not destination:
        raise AppError("One or both cities not found", 404)

    distance = 0.0
    if origin.latitude and origin.longitude and destination.latitude and destination.longitude:
        distance = _haversine_km(
            float(origin.latitude), float(origin.longitude),
            float(destination.latitude), float(destination.longitude),
        )

    user_message = transport_recommendation.build_prompt(
        origin_city=origin.name,
        origin_country=origin.country,
        destination_city=destination.name,
        destination_country=destination.country,
        distance_km=distance,
        travel_date=data.get("travel_date", ""),
        priority=data.get("priority", "cost"),
        group_size=data.get("group_size", 1),
        budget_usd=data.get("budget_usd", 100),
        flight_data=flight_data,
    )

    system = _user_system_prompt(user)
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]

    raw, is_fallback = _safe_call_ai(
        messages,
        feature_key="recommend-transport",
        temperature=transport_recommendation.TEMPERATURE,
        max_tokens=transport_recommendation.MAX_TOKENS,
    )

    if is_fallback:
        return {"error": "ai_unavailable", "message": raw}

    parsed = _parse_json_response(raw)
    return parsed if parsed is not None else {"error": "parse_error", "message": raw}


# ---------------------------------------------------------------------------
# Feature: Review Trip
# ---------------------------------------------------------------------------

def review_trip(user: User, trip_slug: str) -> dict:
    trip = _load_trip_with_stops(trip_slug, user)
    stops = trip.stops.order_by(Stop.order_index).all()

    stops_context = []
    city_seasonal = []
    total_budget = 0.0

    for stop in stops:
        city = stop.city
        activities_data = []
        for sa in stop.stop_activities.all():
            cost = float(sa.custom_cost_usd or (sa.activity.cost_usd if sa.activity else 0) or 0)
            total_budget += cost
            activities_data.append(
                {
                    "name": sa.activity.name if sa.activity else sa.custom_name,
                    "category": sa.category.value if hasattr(sa.category, "value") else sa.category,
                    "scheduled_date": str(sa.scheduled_date) if sa.scheduled_date else None,
                    "cost_usd": cost,
                }
            )

        stops_context.append(
            {
                "city": city.name,
                "arrival_date": str(stop.arrival_date),
                "departure_date": str(stop.departure_date),
                "activities": activities_data,
            }
        )
        city_seasonal.append(
            {
                "city": city.name,
                "best_time_months": city.best_time_months or [],
                "travel_month": stop.arrival_date.month,
            }
        )

    total_days = (trip.end_date - trip.start_date).days + 1

    user_message = trip_feedback.build_prompt(
        trip_name=trip.name,
        trip_start_date=str(trip.start_date),
        trip_end_date=str(trip.end_date),
        total_days=total_days,
        total_budget_usd=total_budget,
        stops_with_activities=stops_context,
        city_seasonal_data=city_seasonal,
    )

    system = _user_system_prompt(user, active_trip=trip)
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]

    raw, is_fallback = _safe_call_ai(
        messages,
        feature_key="review-trip",
        temperature=trip_feedback.TEMPERATURE,
        max_tokens=trip_feedback.MAX_TOKENS,
    )

    if is_fallback:
        return {"error": "ai_unavailable", "message": raw}

    parsed = _parse_json_response(raw)
    return parsed if parsed is not None else {"error": "parse_error", "message": raw}


# ---------------------------------------------------------------------------
# Feature: Packing Advice
# ---------------------------------------------------------------------------

def packing_advice(user: User, trip_slug: str, existing_item_names: list[str]) -> dict:
    trip = _load_trip_with_stops(trip_slug, user)
    stops = trip.stops.order_by(Stop.order_index).all()

    cities_data = [
        {
            "city": s.city.name,
            "country": s.city.country,
            "arrival_date": str(s.arrival_date),
            "departure_date": str(s.departure_date),
            "best_time_months": s.city.best_time_months or [],
        }
        for s in stops
    ]

    # Collect unique activity categories for context
    activity_categories: set[str] = set()
    for stop in stops:
        for sa in stop.stop_activities.all():
            cat = sa.category.value if hasattr(sa.category, "value") else sa.category
            if cat:
                activity_categories.add(cat)

    total_days = (trip.end_date - trip.start_date).days + 1
    city_names = [s.city.name for s in stops]
    weather_summary = (
        f"Trip across {', '.join(city_names)}. "
        "Check city seasonal data for climate context."
    )

    user_message = packing_advice.build_prompt(
        trip_name=trip.name,
        trip_duration_days=total_days,
        cities_data=cities_data,
        weather_summary=weather_summary,
        activities_list=list(activity_categories),
        existing_items=existing_item_names,
    )

    system = _user_system_prompt(user, active_trip=trip)
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]

    raw, is_fallback = _safe_call_ai(
        messages,
        feature_key="packing-advice",
        temperature=packing_advice.TEMPERATURE,
        max_tokens=packing_advice.MAX_TOKENS,
    )

    if is_fallback:
        return {"error": "ai_unavailable", "message": raw}

    parsed = _parse_json_response(raw)
    return parsed if parsed is not None else {"error": "parse_error", "message": raw}


# ---------------------------------------------------------------------------
# Feature: Chatbot
# ---------------------------------------------------------------------------

def chat(user: User, messages_history: list[dict], context: dict | None = None) -> dict:
    context = context or {}
    active_trip = None
    active_trip_slug = context.get("active_trip_slug")
    if active_trip_slug:
        active_trip = Trip.query.filter_by(slug=active_trip_slug, user_id=user.id).first()

    stop_names = None
    active_trip_dates = None
    if active_trip:
        stops = active_trip.stops.order_by(Stop.order_index).all()
        stop_names = [s.city.name for s in stops]
        active_trip_dates = f"{active_trip.start_date} to {active_trip.end_date}"

    system_base = _user_system_prompt(
        user,
        current_page=context.get("current_page"),
        active_trip=active_trip,
    )

    system_content = chatbot.build_system(
        base_system=system_base,
        active_trip_name=active_trip.name if active_trip else None,
        active_trip_dates=active_trip_dates,
        active_trip_stops=stop_names,
        active_trip_slug=active_trip_slug,
        username=user.username,
        current_page=context.get("current_page"),
    )

    messages = [{"role": "system", "content": system_content}] + messages_history[-10:]

    raw, is_fallback = _safe_call_ai(
        messages,
        feature_key="chat",
        temperature=chatbot.TEMPERATURE,
        max_tokens=chatbot.MAX_TOKENS,
    )

    if is_fallback:
        return {"reply": raw, "suggested_actions": []}

    clean_text, actions = chatbot.parse_actions(raw)
    return {"reply": clean_text, "suggested_actions": actions}
