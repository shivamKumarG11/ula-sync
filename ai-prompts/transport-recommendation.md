# Transport Recommendation Prompt

**Version:** 1.0.0
**Endpoint:** `POST /api/v1/ai/recommend-transport`
**Temperature:** 0.3
**Max tokens:** 900

---

## Context Variables Injected at Runtime

| Variable | Source |
|---|---|
| `{{origin_city}}` | cities.name |
| `{{destination_city}}` | cities.name |
| `{{origin_country}}` | cities.country |
| `{{destination_country}}` | cities.country |
| `{{distance_km}}` | Computed from lat/lng using Haversine formula |
| `{{travel_date}}` | Request body |
| `{{priority}}` | Request body: speed / cost / comfort / experience |
| `{{group_size}}` | Request body |
| `{{budget_usd}}` | Request body |
| `{{flight_data_json}}` | Live flight data from Amadeus (if available), else "not available" |

---

## User Message Template

```
I need to travel from {{origin_city}} ({{origin_country}}) to {{destination_city}} ({{destination_country}}) on {{travel_date}}.

Distance: approximately {{distance_km}} km
Group size: {{group_size}} people
My priority: {{priority}}
Budget per person: up to ${{budget_usd}}

Live flight data:
{{flight_data_json}}

Please compare the realistic transport options for this route (flight, train, bus, cab/taxi, or combinations). For each option that makes sense for this route:

1. Estimated travel time (door-to-door, not just transit time)
2. Estimated cost per person in USD
3. Pros and cons (2–3 bullet points each)
4. Booking tips (where to book, how far in advance)

Then give a clear VERDICT: which option do you recommend for someone whose priority is {{priority}}, and why in 2–3 sentences.

Return as JSON:
{
  "options": [
    {
      "mode": "flight|train|bus|cab|ferry",
      "duration_hours": 2.5,
      "cost_per_person_usd": 45,
      "pros": ["fast", "comfortable"],
      "cons": ["expensive", "airport transfer adds 1 hour"],
      "booking_tip": "Book on MakeMyTrip or IRCTC at least 3 weeks ahead"
    }
  ],
  "verdict": {
    "recommended_mode": "train",
    "reason": "For a group of 2 prioritising cost, the overnight train saves a hotel night and is much cheaper than flying."
  }
}

If you don't have enough information about this specific route, say so clearly but still give your best general guidance.
```

---

## Notes

- This prompt is triggered from the Trip Flights page ("Should I fly or take a train?" button per leg)
- The live Amadeus flight data for that leg is injected if available
- The recommendation is shown in a modal overlay above the FlightCard results
- User can dismiss it and proceed with manual selection
