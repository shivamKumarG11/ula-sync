# Packing Advice Prompt

**Version:** 1.0.0
**Endpoint:** `POST /api/v1/ai/packing-advice`
**Temperature:** 0.5
**Max tokens:** 800

---

## Context Variables Injected at Runtime

| Variable | Source |
|---|---|
| `{{trip_name}}` | trips.name |
| `{{cities_json}}` | Array of city names with their travel months |
| `{{weather_summary}}` | Summary of weather conditions per city (from Open-Meteo cache or best_time_months) |
| `{{trip_duration_days}}` | computed |
| `{{activities_list}}` | Categories of planned activities (e.g., "trekking, swimming, temple visits, city walks") |
| `{{existing_items}}` | Names of items already in the packing list |

---

## User Message Template

```
I'm going on a {{trip_duration_days}}-day trip called "{{trip_name}}".

Cities and timing:
{{cities_json}}

Expected weather:
{{weather_summary}}

Planned activities include: {{activities_list}}

I've already packed: {{existing_items}}

Please suggest additional packing items I should add. Focus on:
1. Items specifically needed for the weather and climate of these destinations
2. Items for the specific activities I've planned (trekking gear, swimwear, temple dress code, etc.)
3. Essential documents and travel items I haven't mentioned
4. Any destination-specific items (e.g., mosquito repellent for humid cities, altitude medicine for high-altitude stops)

Do NOT suggest items I've already listed.

Return as JSON:
{
  "suggestions": [
    {
      "name": "item name",
      "category": "clothing|documents|electronics|toiletries|medicine|other",
      "is_compulsory": true,
      "reason": "one-sentence explanation of why this matters for my specific trip"
    }
  ]
}

Keep the list practical — max 15 suggestions. Prioritise genuinely trip-specific items over generic travel advice.
```

---

## Notes

- Triggered from the Packing Checklist page via "AI Packing Suggestions" button
- Results shown in a modal with checkboxes — user selects which to add, then clicks "Add Selected"
- `is_compulsory` items are pre-checked in the modal
- After user confirms, a batch POST to `/api/v1/trips/:slug/packing` adds the selected items
