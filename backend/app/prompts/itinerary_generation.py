# PROMPT VERSION: 1.0.0
# Last updated: 2026-05-10
# Feature: Itinerary Generation

import json


TEMPERATURE = 0.8
MAX_TOKENS = 3000


def build_prompt(
    trip_name: str,
    trip_start_date: str,
    trip_end_date: str,
    total_days: int,
    stops_data: list[dict],
    pace: str = "moderate",
    interests: list[str] | None = None,
    budget_level: str = "mid-range",
    avoid: list[str] | None = None,
    preferred_currency: str = "USD",
) -> str:
    stops_json = json.dumps(stops_data, indent=2, ensure_ascii=False)
    interests_str = ", ".join(interests) if interests else "not specified"
    avoid_str = ", ".join(avoid) if avoid else "nothing specific"

    return f"""Please generate a detailed day-by-day itinerary for my trip: "{trip_name}".

Trip details:
- Travel dates: {trip_start_date} to {trip_end_date} ({total_days} days total)
- My travel pace: {pace} (relaxed = fewer activities per day, packed = maximize activities)
- My interests: {interests_str}
- Budget level: {budget_level}
- I want to avoid: {avoid_str}

My stops and available activities:
{stops_json}

Instructions:
1. For each day of each stop, suggest 2–5 activities from the available list (or activities you know are in that city if the list is short)
2. Include approximate timings (morning / afternoon / evening)
3. Note any booking requirements or tips specific to the activity
4. Group meals naturally into the day (breakfast, lunch, dinner) — suggest local food options
5. Respect travel days: if I'm moving between cities, keep that day lighter
6. Add a brief "AI notes" paragraph at the end explaining your overall logic and any trade-offs you made

Return your response as valid JSON in exactly this structure:
{{
  "itinerary": [
    {{
      "stop": "city name",
      "arrival_date": "YYYY-MM-DD",
      "departure_date": "YYYY-MM-DD",
      "days": [
        {{
          "date": "YYYY-MM-DD",
          "theme": "one-phrase theme for the day",
          "activities": [
            {{
              "time": "HH:MM",
              "name": "activity name",
              "category": "sightseeing|food|adventure|shopping|wellness|cultural|transit",
              "duration_hours": 2.0,
              "estimated_cost_usd": 15,
              "notes": "any tips or booking notes"
            }}
          ]
        }}
      ]
    }}
  ],
  "ai_notes": "explanation of your planning logic"
}}

If you cannot generate a full itinerary due to missing data, return:
{{ "error": "insufficient_data", "message": "explanation of what's missing" }}"""
