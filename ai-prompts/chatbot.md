# Chatbot Prompt

**Version:** 1.0.0
**Endpoint:** `POST /api/v1/ai/chat`
**Temperature:** 0.7
**Max tokens:** 600 per turn

---

## Context Variables Injected at Runtime

| Variable | Source |
|---|---|
| `{{username}}` | Auth store |
| `{{preferred_currency}}` | User profile |
| `{{active_trip_name}}` | Active trip from TanStack Query cache (optional) |
| `{{active_trip_dates}}` | Active trip start–end (optional) |
| `{{active_trip_stops}}` | Comma-joined city names (optional) |
| `{{current_page}}` | Current route (from URL) |
| `{{conversation_history}}` | Prior turns in this session |

---

## System Message Template

```
{{system_base}}

{{#if active_trip}}
The user is currently planning: "{{active_trip_name}}" ({{active_trip_dates}}) visiting {{active_trip_stops}}.
Current page: {{current_page}}
{{/if}}

You are having a focused travel planning conversation. Keep responses under 150 words unless the user explicitly asks for a detailed breakdown. Use bullet points for lists. End responses that open a path for action with a relevant suggestion (e.g., "Want me to suggest activities for Jaipur?").

You can suggest the following app actions by including them in your response as [ACTION: label | url] tokens — the frontend will render these as clickable buttons:
- [ACTION: View Jaipur | /cities/jaipur]
- [ACTION: Check weather in Rishikesh | /cities/rishikesh/weather]
- [ACTION: Open Itinerary Builder | /u/{{username}}/trips/{{active_trip_slug}}/build]
- [ACTION: Add city to my trip | /cities/search]
```

---

## Conversation History Format

The full conversation history is sent on every turn:

```json
[
  { "role": "system", "content": "{{system_with_context}}" },
  { "role": "user", "content": "What's the best time to visit Rishikesh?" },
  { "role": "assistant", "content": "February to May is ideal for river rafting..." },
  { "role": "user", "content": "How does it compare to Haridwar?" }
]
```

Maximum history kept: last 10 turns (5 user + 5 assistant). Older turns are dropped client-side to control token usage.

---

## Suggested Actions Parsing

The backend parses `[ACTION: label | url]` tokens from the AI response before returning to the frontend:

```python
import re

def parse_actions(text: str):
    pattern = r'\[ACTION:\s*(.+?)\s*\|\s*(.+?)\]'
    actions = re.findall(pattern, text)
    clean_text = re.sub(pattern, '', text).strip()
    return clean_text, [{"label": a[0], "url": a[1]} for a in actions]
```

The frontend renders these as pill buttons below the chat message.

---

## Example Interaction

**User:** "I have 5 days in Rajasthan. Is that enough?"

**AI response (raw):**
```
5 days is a solid start for Rajasthan! Here's a realistic split:
- **2 days Jaipur** — Amber Fort, City Palace, Hawa Mahal
- **2 days Jodhpur** — Mehrangarh Fort, blue city walks
- **1 day transit/buffer** — or squeeze in Pushkar

You'll have to skip Udaipur and Jaisalmer, which deserve separate trips.

[ACTION: Explore Jaipur | /cities/jaipur]
[ACTION: Explore Jodhpur | /cities/jodhpur]
```

**Rendered to user:**
- Text without action tokens
- Two pill buttons: "Explore Jaipur" and "Explore Jodhpur"

---

## Notes

- The chatbot does NOT have access to real-time data (flights, hotels, live weather) — it uses general knowledge
- For real-time data, the chatbot should direct users to the relevant app pages via action buttons
- Conversation history is stored in React component state — it is cleared when the chat bubble is closed or the page refreshes
- No conversation is stored on the server side in MVP
