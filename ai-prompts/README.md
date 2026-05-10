# AI Prompts

This folder contains the human-readable master versions of all AI prompts used in Traveloop. These are the source of truth — the actual Python prompt constants in `backend/app/prompts/` are generated from these files.

## How to Edit Prompts

1. Edit the `.md` file here
2. Copy the updated prompt text into the corresponding Python file in `backend/app/prompts/`
3. Bump the `PROMPT VERSION` comment in the Python file
4. Test the endpoint manually before merging

## Prompt Files

| File | Feature | Endpoint |
|---|---|---|
| `system-base.md` | Shared persona injected into all calls | All AI endpoints |
| `itinerary-generation.md` | Full day-by-day itinerary generation | `POST /api/v1/ai/generate-itinerary` |
| `activity-suggestions.md` | City activity suggestions based on preferences | `POST /api/v1/ai/suggest-activities` |
| `transport-recommendation.md` | Flight vs train vs bus vs cab recommendation | `POST /api/v1/ai/recommend-transport` |
| `trip-feedback.md` | Trip plan review and scoring | `POST /api/v1/ai/review-trip` |
| `packing-advice.md` | Packing list suggestions based on trip + weather | `POST /api/v1/ai/packing-advice` |
| `chatbot.md` | General travel assistant chatbot | `POST /api/v1/ai/chat` |

## Prompt Design Rules

1. **Output format is always specified explicitly** — every prompt that returns structured data tells the model exactly what JSON shape to produce
2. **Fallback instructions are included** — every prompt tells the model what to do if it lacks enough data
3. **Context variables are marked with `{{double_braces}}`** — these are replaced at runtime by `ai_service.py`
4. **Persona is always the system message** — user data goes in the user message, never the system message
5. **Temperature guidance**: generation prompts use 0.8 (creative), review/feedback prompts use 0.3 (analytical), chatbot uses 0.7 (balanced)
