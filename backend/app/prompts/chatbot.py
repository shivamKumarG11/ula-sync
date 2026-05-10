# PROMPT VERSION: 1.0.0
# Last updated: 2026-05-10
# Feature: Global AI Chatbot

import re


TEMPERATURE = 0.7
MAX_TOKENS = 600


def build_system(
    base_system: str,
    active_trip_name: str | None = None,
    active_trip_dates: str | None = None,
    active_trip_stops: list[str] | None = None,
    active_trip_slug: str | None = None,
    username: str | None = None,
    current_page: str | None = None,
) -> str:
    lines = [base_system, ""]

    if active_trip_name and active_trip_dates:
        stops_str = ", ".join(active_trip_stops) if active_trip_stops else ""
        lines.append(
            f'The user is currently planning: "{active_trip_name}" ({active_trip_dates})'
            + (f" visiting {stops_str}." if stops_str else ".")
        )

    if current_page:
        lines.append(f"Current page: {current_page}")

    lines.append(
        "\nYou are having a focused travel planning conversation. Keep responses under 150 words "
        "unless the user explicitly asks for a detailed breakdown. Use bullet points for lists. "
        "End responses that open a path for action with a relevant suggestion."
    )

    if username and active_trip_slug:
        lines.append(
            "\nYou can suggest app actions by including [ACTION: label | url] tokens — "
            "the frontend renders these as clickable buttons:\n"
            "Examples:\n"
            "- [ACTION: View Jaipur | /cities/jaipur]\n"
            f"- [ACTION: Open Itinerary Builder | /u/{username}/trips/{active_trip_slug}/build]"
        )

    return "\n".join(lines)


def parse_actions(text: str) -> tuple[str, list[dict]]:
    """Extract [ACTION: label | url] tokens and return (clean_text, actions_list)."""
    pattern = r"\[ACTION:\s*(.+?)\s*\|\s*(.+?)\]"
    actions = [{"label": m[0], "url": m[1]} for m in re.findall(pattern, text)]
    clean_text = re.sub(pattern, "", text).strip()
    return clean_text, actions
