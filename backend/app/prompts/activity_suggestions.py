# PROMPT VERSION: 1.0.0
# Last updated: 2026-05-10
# Feature: Activity Suggestions

import json


TEMPERATURE = 0.75
MAX_TOKENS = 1200


def build_prompt(
    city_name: str,
    city_country: str,
    city_description: str,
    days_available: int,
    budget_usd_per_day: float,
    user_interests: list[str],
    catalog_activities: list[dict],
    existing_activity_names: list[str] | None = None,
) -> str:
    catalog_json = json.dumps(catalog_activities, indent=2, ensure_ascii=False)
    interests_str = ", ".join(user_interests) if user_interests else "general sightseeing"
    existing_str = ", ".join(existing_activity_names) if existing_activity_names else "none yet"

    return f"""I'm visiting {city_name}, {city_country} for {days_available} days with a budget of approximately ${budget_usd_per_day} per day.

My interests: {interests_str}

About the city: {city_description}

Available catalog activities:
{catalog_json}

Already added to my itinerary: {existing_str}

Please suggest 6–10 activities I should consider, prioritising those that match my interests and fit my budget. For each suggestion:
- Explain in one sentence WHY this activity fits my travel style
- Include if it needs advance booking
- If the activity is from the catalog above, use that name exactly
- You may suggest activities NOT in the catalog if they are well-known and genuinely worth recommending

Return as JSON:
{{
  "suggestions": [
    {{
      "name": "activity name",
      "category": "sightseeing|food|adventure|shopping|wellness|cultural|other",
      "estimated_cost_usd": 20,
      "duration_hours": 2.5,
      "why_fits": "one sentence explanation",
      "booking_required": true,
      "from_catalog": true
    }}
  ]
}}"""
