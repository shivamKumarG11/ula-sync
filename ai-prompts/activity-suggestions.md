# Activity Suggestions Prompt

**Version:** 1.0.0
**Endpoint:** `POST /api/v1/ai/suggest-activities`
**Temperature:** 0.75
**Max tokens:** 1200

---

## Context Variables Injected at Runtime

| Variable | Source |
|---|---|
| `{{city_name}}` | cities.name |
| `{{city_country}}` | cities.country |
| `{{city_description}}` | cities.description |
| `{{days_available}}` | Request body |
| `{{budget_usd_per_day}}` | Request body |
| `{{user_interests}}` | Request body: comma-joined array |
| `{{catalog_activities_json}}` | Array of catalog activities for this city (name, category, cost_usd, duration_hours, description) |
| `{{existing_activities}}` | Names of activities already added, to avoid duplicates |

---

## User Message Template

```
I'm visiting {{city_name}}, {{city_country}} for {{days_available}} days with a budget of approximately ${{budget_usd_per_day}} per day.

My interests: {{user_interests}}

About the city: {{city_description}}

Available catalog activities:
{{catalog_activities_json}}

Already added to my itinerary: {{existing_activities}}

Please suggest 6–10 activities I should consider, prioritising those that match my interests and fit my budget. For each suggestion:
- Explain in one sentence WHY this activity fits my travel style
- Include if it needs advance booking
- If the activity is from the catalog above, use that name exactly
- You may suggest activities NOT in the catalog if they are well-known and genuinely worth recommending

Return as JSON:
{
  "suggestions": [
    {
      "name": "activity name",
      "category": "sightseeing|food|adventure|shopping|wellness|cultural|other",
      "estimated_cost_usd": 20,
      "duration_hours": 2.5,
      "why_fits": "one sentence explanation",
      "booking_required": true,
      "from_catalog": true
    }
  ]
}
```

---

## Notes

- This prompt fires automatically when a user adds a new stop city in the Itinerary Builder
- Results are shown in the `AIAssistPanel` alongside the activity catalog
- The user can dismiss or add any suggestion with one click
- Suggestions that are already in the user's stop activities are filtered out client-side before display
