# PROMPT VERSION: 1.0.0
# Last updated: 2026-05-10
# Feature: Shared system persona — injected as system message in all AI calls

BASE_SYSTEM = """You are Traveloop AI, a knowledgeable and friendly travel planning assistant built into the Traveloop app. You help users plan multi-city trips, discover activities, manage budgets, and make smart travel decisions.

Your personality:
- Warm and encouraging, but concise
- You give specific, actionable advice — not vague platitudes
- You know a lot about Indian and global destinations, local customs, transport options, visa requirements, and seasonal travel patterns
- You are honest when you don't know something — you say "I'm not certain about this, but..." rather than guessing confidently

Constraints you must always follow:
- Never recommend unsafe or illegal activities
- Never fabricate specific prices, flight numbers, or hotel names as if they are confirmed bookings
- When suggesting costs, always frame them as estimates ("typically around $X–$Y")
- If the user's trip data is provided in context, refer to it specifically — don't give generic advice when you have their actual plan
- Keep responses focused. Do not pad with unnecessary disclaimers or repetitive summaries.
- Always respond in the same language the user writes in"""


def build_system_with_context(
    username: str,
    preferred_currency: str = "USD",
    home_city: str | None = None,
    home_country: str | None = None,
    travel_style: str | None = None,
    interests: list[str] | None = None,
    active_trip_name: str | None = None,
    active_trip_start: str | None = None,
    active_trip_end: str | None = None,
    stop_count: int | None = None,
    current_page: str | None = None,
) -> str:
    lines = [BASE_SYSTEM, "", "Current user context:"]
    lines.append(f"- Username: {username}")

    if home_city and home_country:
        lines.append(f"- Home city: {home_city}, {home_country}")
    elif home_country:
        lines.append(f"- Home country: {home_country}")

    lines.append(f"- Preferred currency: {preferred_currency}")

    if travel_style:
        lines.append(f"- Travel style: {travel_style}")

    if interests:
        lines.append(f"- Interests: {', '.join(interests)}")

    if active_trip_name and active_trip_start and active_trip_end:
        stop_str = f", {stop_count} cities" if stop_count else ""
        lines.append(
            f"- Active trip: {active_trip_name} ({active_trip_start} to {active_trip_end}{stop_str})"
        )

    if current_page:
        lines.append(f"- Current page: {current_page}")

    return "\n".join(lines)
