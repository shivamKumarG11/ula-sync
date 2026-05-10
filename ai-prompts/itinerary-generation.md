# Itinerary Generation Prompt

**Version:** 1.0.0
**Endpoint:** `POST /api/v1/ai/generate-itinerary`
**Temperature:** 0.8
**Max tokens:** 3000

---

## Context Variables Injected at Runtime

| Variable | Source |
|---|---|
| `{{trip_name}}` | trips.name |
| `{{trip_start_date}}` | trips.start_date |
| `{{trip_end_date}}` | trips.end_date |
| `{{total_days}}` | computed |
| `{{stops_json}}` | Array of stops with city name, arrival/departure dates, available activities (name, category, cost, duration) |
| `{{user_pace}}` | Request body: preferences.pace |
| `{{user_interests}}` | Request body: preferences.interests (comma-joined) |
| `{{budget_level}}` | Request body: preferences.budget_level |
| `{{avoid_list}}` | Request body: preferences.avoid (comma-joined, or "nothing specific") |
| `{{preferred_currency}}` | User profile |

---

## System Message

Uses `system-base.md` + active trip context block.

---

## User Message Template

```
Please generate a detailed day-by-day itinerary for my trip: "{{trip_name}}".

Trip details:
- Travel dates: {{trip_start_date}} to {{trip_end_date}} ({{total_days}} days total)
- My travel pace: {{user_pace}} (relaxed = fewer activities per day, packed = maximize activities)
- My interests: {{user_interests}}
- Budget level: {{budget_level}}
- I want to avoid: {{avoid_list}}

My stops and available activities:
{{stops_json}}

Instructions:
1. For each day of each stop, suggest 2–5 activities from the available list (or activities you know are in that city if the list is short)
2. Include approximate timings (morning / afternoon / evening)
3. Note any booking requirements or tips specific to the activity
4. Group meals naturally into the day (breakfast, lunch, dinner) — suggest local food options
5. Respect travel days: if I'm moving between cities, keep that day lighter
6. Add a brief "AI notes" paragraph at the end explaining your overall logic and any trade-offs you made

Return your response as valid JSON in exactly this structure:
{
  "itinerary": [
    {
      "stop": "city name",
      "arrival_date": "YYYY-MM-DD",
      "departure_date": "YYYY-MM-DD",
      "days": [
        {
          "date": "YYYY-MM-DD",
          "theme": "one-phrase theme for the day",
          "activities": [
            {
              "time": "HH:MM",
              "name": "activity name",
              "category": "sightseeing|food|adventure|shopping|wellness|cultural|transit",
              "duration_hours": 2.0,
              "estimated_cost_usd": 15,
              "notes": "any tips or booking notes"
            }
          ]
        }
      ]
    }
  ],
  "ai_notes": "explanation of your planning logic"
}

If you cannot generate a full itinerary due to missing data, return:
{ "error": "insufficient_data", "message": "explanation of what's missing" }
```
