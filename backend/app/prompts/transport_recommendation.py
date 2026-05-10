# PROMPT VERSION: 1.0.0
# Last updated: 2026-05-10
# Feature: Transport Recommendation

import json


TEMPERATURE = 0.3
MAX_TOKENS = 900


def build_prompt(
    origin_city: str,
    origin_country: str,
    destination_city: str,
    destination_country: str,
    distance_km: float,
    travel_date: str,
    priority: str,
    group_size: int,
    budget_usd: float,
    flight_data: dict | list | None = None,
) -> str:
    flight_json = json.dumps(flight_data, ensure_ascii=False) if flight_data else "not available"

    return f"""I need to travel from {origin_city} ({origin_country}) to {destination_city} ({destination_country}) on {travel_date}.

Distance: approximately {distance_km:.0f} km
Group size: {group_size} people
My priority: {priority}
Budget per person: up to ${budget_usd}

Live flight data:
{flight_json}

Please compare the realistic transport options for this route (flight, train, bus, cab/taxi, or combinations). For each option that makes sense for this route:

1. Estimated travel time (door-to-door, not just transit time)
2. Estimated cost per person in USD
3. Pros and cons (2–3 bullet points each)
4. Booking tips (where to book, how far in advance)

Then give a clear VERDICT: which option do you recommend for someone whose priority is {priority}, and why in 2–3 sentences.

Return as JSON:
{{
  "options": [
    {{
      "mode": "flight|train|bus|cab|ferry",
      "duration_hours": 2.5,
      "cost_per_person_usd": 45,
      "pros": ["fast", "comfortable"],
      "cons": ["expensive", "airport transfer adds 1 hour"],
      "booking_tip": "Book on MakeMyTrip or IRCTC at least 3 weeks ahead"
    }}
  ],
  "verdict": {{
    "recommended_mode": "train",
    "reason": "For a group of 2 prioritising cost, the overnight train saves a hotel night and is much cheaper than flying."
  }}
}}

If you don't have enough information about this specific route, say so clearly but still give your best general guidance."""
