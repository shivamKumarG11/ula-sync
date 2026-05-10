# Trip Feedback / Review Prompt

**Version:** 1.0.0
**Endpoint:** `POST /api/v1/ai/review-trip`
**Temperature:** 0.3
**Max tokens:** 1500

---

## Context Variables Injected at Runtime

| Variable | Source |
|---|---|
| `{{trip_name}}` | trips.name |
| `{{trip_start_date}}` | trips.start_date |
| `{{trip_end_date}}` | trips.end_date |
| `{{total_days}}` | computed |
| `{{total_budget_usd}}` | computed from budget breakdown |
| `{{stops_with_activities_json}}` | Full itinerary: stops with activities, dates, costs |
| `{{city_seasonal_data}}` | For each city: best_time_months, typical weather in travel month |

---

## User Message Template

```
Please review my travel plan and give me honest, actionable feedback.

Trip: "{{trip_name}}"
Dates: {{trip_start_date}} to {{trip_end_date}} ({{total_days}} days)
Total estimated budget: ${{total_budget_usd}} USD

Full itinerary:
{{stops_with_activities_json}}

City seasonal context:
{{city_seasonal_data}}

Review my trip across these dimensions:
1. **Pacing** — Are the days too packed or too empty? Is the overall pace realistic?
2. **Budget** — Is my estimated spend reasonable for these destinations? Any red flags?
3. **Seasonality** — Am I visiting each city in a good season? Any weather concerns?
4. **Logistics** — Are the city transitions smooth? Any transit gaps or tight connections?
5. **Coverage** — Am I missing any unmissable experiences in these cities given my activities?
6. **Balance** — Is there a good mix of activity types (sightseeing, food, rest)?

For each issue you find, classify it as:
- "warning" — something that could meaningfully hurt the trip
- "tip" — a nice-to-know improvement
- "praise" — something you did well (at least 2 praises required)

Return as JSON:
{
  "score": 85,
  "summary": "2-3 sentence overall assessment",
  "feedback": [
    {
      "dimension": "pacing|budget|seasonality|logistics|coverage|balance",
      "severity": "warning|tip|praise",
      "message": "specific, actionable feedback"
    }
  ],
  "top_suggestions": [
    "concrete suggestion 1",
    "concrete suggestion 2",
    "concrete suggestion 3"
  ]
}

Score: 0–100. 90+ = excellent, 75–89 = good, 60–74 = needs improvement, below 60 = significant issues.
Be honest — a low score with clear suggestions is more useful than a high score with vague praise.
```

---

## Notes

- Triggered from the Itinerary View page via "Review My Trip" button
- Result displayed in the `AIAssistPanel` component with score badge, summary, and expandable feedback cards
- Warnings shown in orange, tips in blue, praises in green
- "Top suggestions" shown as action-buttons where possible (e.g., "Add an evening activity on Day 3" → links to builder)
