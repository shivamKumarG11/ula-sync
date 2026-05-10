# PROMPT VERSION: 1.0.0
# Last updated: 2026-05-10
# Feature: Packing Advice

import json


TEMPERATURE = 0.5
MAX_TOKENS = 800


def build_prompt(
    trip_name: str,
    trip_duration_days: int,
    cities_data: list[dict],
    weather_summary: str,
    activities_list: list[str],
    existing_items: list[str],
) -> str:
    cities_json = json.dumps(cities_data, indent=2, ensure_ascii=False)
    activities_str = ", ".join(activities_list) if activities_list else "general sightseeing"
    existing_str = ", ".join(existing_items) if existing_items else "nothing yet"

    return f"""I'm going on a {trip_duration_days}-day trip called "{trip_name}".

Cities and timing:
{cities_json}

Expected weather:
{weather_summary}

Planned activities include: {activities_str}

I've already packed: {existing_str}

Please suggest additional packing items I should add. Focus on:
1. Items specifically needed for the weather and climate of these destinations
2. Items for the specific activities I've planned (trekking gear, swimwear, temple dress code, etc.)
3. Essential documents and travel items I haven't mentioned
4. Any destination-specific items (e.g., mosquito repellent for humid cities, altitude medicine for high-altitude stops)

Do NOT suggest items I've already listed.

Return as JSON:
{{
  "suggestions": [
    {{
      "name": "item name",
      "category": "clothing|documents|electronics|toiletries|medicine|other",
      "is_compulsory": true,
      "reason": "one-sentence explanation of why this matters for my specific trip"
    }}
  ]
}}

Keep the list practical — max 15 suggestions. Prioritise genuinely trip-specific items over generic travel advice."""
