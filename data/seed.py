#!/usr/bin/env python3
"""
seed.py — City data sync: Markdown → JSON → PostgreSQL

Reads each city's .md file, generates a .json in the same folder,
then upserts the data into PostgreSQL (cities, city_cost_breakdown, activities).

Running the script again after editing a .md re-generates the JSON and
updates the DB — fully idempotent.

Usage:
    python seed.py              # process all cities
    python seed.py singapore    # process one city by slug

Requirements:
    pip install psycopg2-binary python-dotenv

DATABASE_URL must be set in the environment or in a .env file
(looks 3 levels up from this file, i.e. the project root).

If DATABASE_URL is not set the script still runs in JSON-only mode.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Optional dependencies — graceful fallback if missing
# ---------------------------------------------------------------------------
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    print("Warning: psycopg2 not installed. Running in JSON-only mode.")

try:
    from dotenv import load_dotenv
    # Walk up to find .env in the project root
    _env_path = Path(__file__).parents[3] / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
    else:
        load_dotenv()
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).parent
DB_URL = os.getenv("DATABASE_URL")

# Static metadata for the 17 seeded cities (not in the .md files)
CITY_META: dict[str, dict] = {
    "bali":           {"country": "Indonesia",    "country_code": "ID", "timezone": "Asia/Makassar",      "iata_code": "DPS", "popularity_score": 90},
    "cape-town":      {"country": "South Africa", "country_code": "ZA", "timezone": "Africa/Johannesburg","iata_code": "CPT", "popularity_score": 80},
    "coimbatore":     {"country": "India",        "country_code": "IN", "timezone": "Asia/Kolkata",       "iata_code": "CJB", "popularity_score": 45},
    "dubai":          {"country": "UAE",          "country_code": "AE", "timezone": "Asia/Dubai",         "iata_code": "DXB", "popularity_score": 95},
    "hampi":          {"country": "India",        "country_code": "IN", "timezone": "Asia/Kolkata",       "iata_code": "HBX", "popularity_score": 55},
    "jaipur":         {"country": "India",        "country_code": "IN", "timezone": "Asia/Kolkata",       "iata_code": "JAI", "popularity_score": 75},
    "kyoto":          {"country": "Japan",        "country_code": "JP", "timezone": "Asia/Tokyo",         "iata_code": "ITM", "popularity_score": 88},
    "nalanda":        {"country": "India",        "country_code": "IN", "timezone": "Asia/Kolkata",       "iata_code": "GAY", "popularity_score": 40},
    "puducherry":     {"country": "India",        "country_code": "IN", "timezone": "Asia/Kolkata",       "iata_code": "PNY", "popularity_score": 50},
    "rio-de-janerio": {"country": "Brazil",       "country_code": "BR", "timezone": "America/Sao_Paulo",  "iata_code": "GIG", "popularity_score": 85},
    "rishikesh":      {"country": "India",        "country_code": "IN", "timezone": "Asia/Kolkata",       "iata_code": "DED", "popularity_score": 60},
    "santorini":      {"country": "Greece",       "country_code": "GR", "timezone": "Europe/Athens",      "iata_code": "JTR", "popularity_score": 92},
    "seoul":          {"country": "South Korea",  "country_code": "KR", "timezone": "Asia/Seoul",         "iata_code": "ICN", "popularity_score": 87},
    "shillong":       {"country": "India",        "country_code": "IN", "timezone": "Asia/Kolkata",       "iata_code": "SHL", "popularity_score": 48},
    "singapore":      {"country": "Singapore",    "country_code": "SG", "timezone": "Asia/Singapore",     "iata_code": "SIN", "popularity_score": 93},
    "sydney":         {"country": "Australia",    "country_code": "AU", "timezone": "Australia/Sydney",   "iata_code": "SYD", "popularity_score": 89},
    "varanasi":       {"country": "India",        "country_code": "IN", "timezone": "Asia/Kolkata",       "iata_code": "VNS", "popularity_score": 70},
    "venice":         {"country": "Italy",        "country_code": "IT", "timezone": "Europe/Rome",        "iata_code": "VCE", "popularity_score": 91},
}

# Maps markdown expense type labels → DB enum values (expense_type_enum)
EXPENSE_TYPE_MAP: dict[str, str] = {
    "travel":                      "travel",
    "stay":                        "stay",
    "food":                        "food",
    "activities & entry tickets":  "activities",
    "activities":                  "activities",
    "local transport":             "local_transport",
    "local transportation":        "local_transport",
}

# All location-type entries land in this category.
# Must match a value in your activity_category_enum.
LOCATION_CATEGORY = "sightseeing"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def parse_time_str(text: str) -> Optional[str]:
    """Convert '10:00 AM', '5:00 AM' → 'HH:MM'. Returns None for 'Open all day' etc."""
    if not text or re.search(r"open all day|all day|open", text, re.IGNORECASE):
        return None
    m = re.search(r"(\d{1,2}):(\d{2})\s*(AM|PM)?", text, re.IGNORECASE)
    if not m:
        return None
    h, mn, meridiem = int(m.group(1)), int(m.group(2)), (m.group(3) or "").upper()
    if meridiem == "PM" and h != 12:
        h += 12
    elif meridiem == "AM" and h == 12:
        h = 0
    return f"{h:02d}:{mn:02d}"


def parse_usd_cost(text: str) -> float:
    """Extract numeric cost from strings like 'SGD 35', '$35', 'Free', 'SGD 83'."""
    if not text or re.search(r"free|none|-", text.strip(), re.IGNORECASE):
        return 0.0
    m = re.search(r"[\d]+(?:\.\d+)?", text)
    return float(m.group()) if m else 0.0


def parse_duration_hours(text: str) -> Optional[float]:
    """Parse '2–4 hours' → 3.0, 'Full day' → 8.0, '30–60 minutes' → 0.75."""
    text = text.lower()
    if "full day" in text:
        return 8.0
    m = re.search(r"(\d+(?:\.\d+)?)\s*[–\-to]+\s*(\d+(?:\.\d+)?)\s*hour", text)
    if m:
        return (float(m.group(1)) + float(m.group(2))) / 2
    m = re.search(r"(\d+(?:\.\d+)?)\s*hour", text)
    if m:
        return float(m.group(1))
    m = re.search(r"(\d+)\s*[–\-to]+\s*(\d+)\s*min", text)
    if m:
        return (float(m.group(1)) + float(m.group(2))) / 2 / 60
    m = re.search(r"(\d+)\s*min", text)
    if m:
        return float(m.group(1)) / 60
    return None


def extract_currency_code(local_col: str) -> str:
    """Extract 3-letter currency code from a column value like 'SGD 120'."""
    m = re.match(r"([A-Z]{3})\b", local_col.strip())
    return m.group(1) if m else "USD"


def find_image_for(folder: Path, item_name: str) -> Optional[str]:
    """
    Fuzzy-match an image in `folder` by item name.
    Returns a path string relative to DATA_DIR (for storing in JSON/DB).
    """
    if not folder.exists():
        return None
    target = slugify(item_name)
    for ext in ("jpg", "jpeg", "png", "webp"):
        for f in folder.glob(f"*.{ext}"):
            if slugify(f.stem) == target:
                return str(f.relative_to(DATA_DIR))
        # Partial match fallback
        for f in folder.glob(f"*.{ext}"):
            stem = slugify(f.stem)
            if target in stem or stem in target:
                return str(f.relative_to(DATA_DIR))
    return None


# ---------------------------------------------------------------------------
# Markdown parsers
# ---------------------------------------------------------------------------

def get_section(heading: str, text: str) -> str:
    """Return the content under a '## Heading' section (stops at next ##)."""
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}.*?\n([\s\S]*?)(?=^##\s|\Z)",
        re.MULTILINE,
    )
    m = pattern.search(text)
    return m.group(1).strip() if m else ""


def parse_cost_table(section_text: str) -> list[dict]:
    """Parse the 'Average Daily Budget Per Person' table."""
    rows: list[dict] = []
    in_table = False
    for line in section_text.splitlines():
        line = line.strip()
        if "|" not in line:
            if in_table:
                break
            continue
        cols = [c.strip() for c in line.split("|") if c.strip()]
        if not cols:
            continue
        first = cols[0].lower()
        if "expense type" in first:
            in_table = True
            continue
        if re.fullmatch(r"[-| ]+", line):
            continue
        if not in_table:
            continue
        if len(cols) < 3:
            continue

        expense_type = None
        for key, val in EXPENSE_TYPE_MAP.items():
            if key in first:
                expense_type = val
                break
        if not expense_type:
            continue

        usd_raw = re.sub(r"[^\d.]", "", cols[1]) or "0"
        local_raw = cols[2]
        local_num = re.sub(r"[^\d.]", "", local_raw) or "0"
        desc = cols[3] if len(cols) > 3 else ""

        rows.append({
            "expense_type": expense_type,
            "cost_usd": float(usd_raw),
            "cost_local": float(local_num),
            "local_currency": extract_currency_code(local_raw),
            "description": desc,
        })
    return rows


def parse_numbered_items(text: str) -> list[dict]:
    """
    Parse numbered list items of the form:
        1. **Item Name**
           Description text here.
    Returns list of {name, description}.
    """
    items: list[dict] = []
    current: Optional[dict] = None

    for line in text.splitlines():
        stripped = line.strip()

        # New numbered item line: "1. **Name**" or "1. Name"
        m = re.match(r"^\d+\.\s+\*{0,2}(.+?)\*{0,2}\s*$", stripped)
        if m:
            if current:
                items.append(current)
            current = {"name": m.group(1).strip(), "description": ""}
            continue

        if current is None:
            continue

        # Skip sub-headings that start new sections
        if stripped.startswith("#"):
            break

        # Accumulate description (skip blank separator lines after first desc line)
        if stripped:
            sep = " " if current["description"] else ""
            current["description"] = current["description"] + sep + stripped

    if current:
        items.append(current)
    return items


def parse_table_rows(text: str) -> list[dict]:
    """
    Parse a generic 3-column markdown table → list of {name, specialty, map_link}.
    Used for food areas and shopping markets.
    """
    rows: list[dict] = []
    header_seen = False
    for line in text.splitlines():
        line = line.strip()
        if "|" not in line:
            continue
        cols = [c.strip() for c in line.split("|") if c.strip()]
        if not cols:
            continue
        if re.fullmatch(r"[-| ]+", line):
            continue
        first_lower = cols[0].lower()
        if not header_seen:
            # Only treat as header when not yet in the table
            if any(k in first_lower for k in ("area name", "market name")):
                header_seen = True
            continue
        rows.append({
            "name": cols[0] if len(cols) > 0 else "",
            "specialty": cols[1] if len(cols) > 1 else "",
            "map_link": cols[2] if len(cols) > 2 else "",
        })
    return rows


def parse_advisories(section_text: str) -> list[str]:
    """Extract bullet-point advisories."""
    advisories = []
    in_advisories = False
    for line in section_text.splitlines():
        stripped = line.strip()
        if re.search(r"travel advisories", stripped, re.IGNORECASE):
            in_advisories = True
            continue
        if re.search(r"packing checklist", stripped, re.IGNORECASE):
            break
        if in_advisories and stripped.startswith("- "):
            advisories.append(stripped[2:].strip())
    return advisories


def parse_packing_checklist(section_text: str) -> dict:
    """Extract compulsory and optional packing items."""
    checklist: dict[str, list[str]] = {"compulsory": [], "optional": []}
    current_bucket: Optional[str] = None

    for line in section_text.splitlines():
        stripped = line.strip()
        if re.search(r"compulsory", stripped, re.IGNORECASE):
            current_bucket = "compulsory"
        elif re.search(r"optional", stripped, re.IGNORECASE):
            current_bucket = "optional"
        elif current_bucket and stripped.startswith("- "):
            checklist[current_bucket].append(stripped[2:].strip())

    return checklist


def parse_locations(locations_text: str) -> list[dict]:
    """
    Parse the '# Famous Locations' section.
    Each location starts with '## Location Name'.
    """
    locations: list[dict] = []

    # Split on '## ' headers (location blocks)
    blocks = re.split(r"\n(?=## )", "\n" + locations_text)
    for block in blocks:
        block = block.strip()
        if not block or not block.startswith("## "):
            continue

        lines = block.splitlines()
        name = lines[0].lstrip("#").strip()
        body = "\n".join(lines[1:])

        # Description
        desc_m = re.search(r"### Description\s*\n([\s\S]*?)(?=###|\Z)", body)
        description = desc_m.group(1).strip() if desc_m else ""

        # Google Map Link
        map_m = re.search(r"### Google Map Link\s*\n- (https?://[^\s\n]+)", body)
        map_link = map_m.group(1).strip() if map_m else ""

        # Visiting time table
        open_m  = re.search(r"\|\s*Opening Time\s*\|\s*(.+?)\s*\|", body)
        close_m = re.search(r"\|\s*Closing Time\s*\|\s*(.+?)\s*\|", body)
        best_m  = re.search(r"\|\s*Best Visiting Time\s*\|\s*(.+?)\s*\|", body)
        opening_time = open_m.group(1).strip()  if open_m  else ""
        closing_time = close_m.group(1).strip() if close_m else ""
        best_visit   = best_m.group(1).strip()  if best_m  else ""

        # Entry cost — prefer foreign tourist cost
        foreign_m = re.search(r"\|\s*Foreign Tourists\s*\|\s*(.+?)\s*\|", body)
        local_m   = re.search(r"\|\s*Local Tourists\s*\|\s*(.+?)\s*\|", body)
        raw_cost  = (foreign_m or local_m)
        cost_usd  = parse_usd_cost(raw_cost.group(1)) if raw_cost else 0.0

        # Duration
        dur_m = re.search(r"### Time Required\s*\n- (.+)", body)
        duration_hours = parse_duration_hours(dur_m.group(1)) if dur_m else None

        # Booking
        book_lines = re.findall(r"### Booking Requirement\s*\n([\s\S]*?)(?=###|\Z)", body)
        book_text = book_lines[0] if book_lines else ""
        booking_required = bool(re.search(r"mandatory|recommended", book_text, re.IGNORECASE))
        book_link_m = re.search(r"(https?://[^\s\n]+)", book_text)
        booking_link = book_link_m.group(1).strip() if book_link_m else ""

        # Example activities
        act_m = re.search(r"### Example Activities.*?\n([\s\S]*?)(?=###|\Z)", body)
        example_activities: list[str] = []
        if act_m:
            for line in act_m.group(1).splitlines():
                stripped = line.strip()
                if stripped.startswith("- "):
                    example_activities.append(stripped[2:].strip())

        locations.append({
            "name": name,
            "description": description,
            "map_link": map_link,
            "opening_time": opening_time,
            "closing_time": closing_time,
            "best_visit_time": best_visit,
            "cost_usd": cost_usd,
            "duration_hours": duration_hours,
            "booking_required": booking_required,
            "booking_link": booking_link if booking_link else None,
            "example_activities": example_activities,
            "image_url": None,  # filled in after image discovery
        })

    return locations


# ---------------------------------------------------------------------------
# Main parse function
# ---------------------------------------------------------------------------

def parse_city_md(city_folder: Path) -> dict:
    city_slug = city_folder.name
    md_path = city_folder / f"{city_slug}.md"
    text = md_path.read_text(encoding="utf-8")

    # City name from # heading
    name_m = re.match(r"^#\s+(.+)", text, re.MULTILINE)
    city_name = name_m.group(1).strip() if name_m else city_slug.replace("-", " ").title()

    # Sections
    description = get_section("Description", text)

    map_m = re.search(r"City Location:\s*(https?://[^\s\n]+)", text)
    map_link = map_m.group(1).strip() if map_m else ""

    best_time_section = get_section("Best Time to Visit", text)
    months_m = re.search(r"Recommended Months:\s*(.+)", best_time_section)
    why_m = re.search(r"Why This Time is Best:\s*(.+)", best_time_section)
    best_time_months = months_m.group(1).strip() if months_m else ""
    best_time_why = why_m.group(1).strip() if why_m else ""

    cost_section = get_section("Cost Index", text)
    cost_rows = parse_cost_table(cost_section)
    budget_m = re.search(r"### Budget Breakdown.*?\n([\s\S]*?)(?=^##|\Z)", cost_section, re.MULTILINE)
    budget_breakdown = budget_m.group(1).strip() if budget_m else ""

    # Daily cost index = sum of local (non-travel) costs
    local_costs = [r["cost_usd"] for r in cost_rows if r["expense_type"] != "travel"]
    cost_index_usd = round(sum(local_costs), 2)

    # Food
    food_section = get_section("Popular Food Items to Eat", text)
    food_list_text = re.split(r"^###", food_section, maxsplit=1, flags=re.MULTILINE)[0]
    food_items = parse_numbered_items(food_list_text)
    food_areas = parse_table_rows(food_section)

    # Things to buy
    buy_section = get_section("Famous Things to Buy", text)
    buy_list_text = re.split(r"^###", buy_section, maxsplit=1, flags=re.MULTILINE)[0]
    buy_items = parse_numbered_items(buy_list_text)
    shopping_markets = parse_table_rows(buy_section)

    # Advisories & packing
    carry_section = get_section("Things to Carry While Travelling and Advisories", text)
    travel_advisories = parse_advisories(carry_section)
    packing_checklist = parse_packing_checklist(carry_section)

    # Famous Locations (under single-# heading)
    loc_heading_m = re.search(r"^# Famous Locations\s*\n([\s\S]+)", text, re.MULTILINE)
    locations_text = loc_heading_m.group(1).strip() if loc_heading_m else ""
    locations = parse_locations(locations_text)

    # ---------- Image discovery ----------
    food_dir  = city_folder / "food"
    loc_dir   = city_folder / "locations"
    buy_dir   = city_folder / "things-to-buy"

    cover_file = city_folder / f"{city_slug}.jpg"
    cover_photo_url = (
        str(cover_file.relative_to(DATA_DIR))
        if cover_file.exists()
        else None
    )

    for item in food_items:
        item["image_url"] = find_image_for(food_dir, item["name"])

    for loc in locations:
        loc["image_url"] = find_image_for(loc_dir, loc["name"])

    for item in buy_items:
        item["image_url"] = find_image_for(buy_dir, item["name"])

    meta = CITY_META.get(city_slug, {})

    return {
        "slug": city_slug,
        "name": city_name,
        "country": meta.get("country", ""),
        "country_code": meta.get("country_code"),
        "timezone": meta.get("timezone"),
        "iata_code": meta.get("iata_code"),
        "popularity_score": meta.get("popularity_score", 50),
        "description": description,
        "cover_photo_url": cover_photo_url,
        "map_link": map_link,
        "best_time_months": best_time_months,
        "best_time_why": best_time_why,
        "cost_index_usd": cost_index_usd,
        "budget_breakdown": budget_breakdown,
        "cost_breakdown": cost_rows,
        "food_items": food_items,
        "food_areas": food_areas,
        "buy_items": buy_items,
        "shopping_markets": shopping_markets,
        "travel_advisories": travel_advisories,
        "packing_checklist": packing_checklist,
        "locations": locations,
    }


# ---------------------------------------------------------------------------
# Database upserts
# ---------------------------------------------------------------------------

def upsert_city(cur, data: dict) -> str:
    cur.execute(
        """
        INSERT INTO cities (
            slug, name, country, country_code, description, cover_photo_url,
            map_link, best_time_months, cost_index_usd, popularity_score,
            timezone, iata_code, created_at
        ) VALUES (
            %(slug)s, %(name)s, %(country)s, %(country_code)s, %(description)s,
            %(cover_photo_url)s, %(map_link)s, %(best_time_months)s,
            %(cost_index_usd)s, %(popularity_score)s, %(timezone)s, %(iata_code)s,
            NOW()
        )
        ON CONFLICT (slug) DO UPDATE SET
            name             = EXCLUDED.name,
            country          = EXCLUDED.country,
            country_code     = EXCLUDED.country_code,
            description      = EXCLUDED.description,
            cover_photo_url  = EXCLUDED.cover_photo_url,
            map_link         = EXCLUDED.map_link,
            best_time_months = EXCLUDED.best_time_months,
            cost_index_usd   = EXCLUDED.cost_index_usd,
            popularity_score = EXCLUDED.popularity_score,
            timezone         = EXCLUDED.timezone,
            iata_code        = EXCLUDED.iata_code
        RETURNING id
        """,
        data,
    )
    return cur.fetchone()["id"]


def upsert_cost_breakdown(cur, city_id: str, rows: list[dict]) -> None:
    cur.execute("DELETE FROM city_cost_breakdown WHERE city_id = %s", (city_id,))
    for row in rows:
        cur.execute(
            """
            INSERT INTO city_cost_breakdown
                (city_id, expense_type, cost_usd, cost_local, local_currency, description)
            VALUES (%s, %s::expense_type_enum, %s, %s, %s, %s)
            """,
            (city_id, row["expense_type"], row["cost_usd"],
             row["cost_local"], row["local_currency"], row["description"]),
        )


def upsert_activities(cur, city_id: str, locations: list[dict]) -> None:
    """
    Each Famous Location becomes a catalog activity (category = 'sightseeing').
    We delete all catalog activities for the city and re-insert so edits to
    the .md are always reflected.
    """
    cur.execute("DELETE FROM activities WHERE city_id = %s", (city_id,))
    for loc in locations:
        cur.execute(
            """
            INSERT INTO activities (
                city_id, name, description, category, cost_usd, duration_hours,
                image_url, map_link, opening_time, closing_time,
                booking_required, booking_link, created_at
            ) VALUES (%s, %s, %s, %s::activity_category_enum, %s, %s, %s, %s,
                      %s, %s, %s, %s, NOW())
            """,
            (
                city_id,
                loc["name"],
                loc["description"],
                LOCATION_CATEGORY,
                loc["cost_usd"],
                loc.get("duration_hours"),
                loc.get("image_url"),
                loc.get("map_link") or None,
                parse_time_str(loc.get("opening_time", "")),
                parse_time_str(loc.get("closing_time", "")),
                loc.get("booking_required", False),
                loc.get("booking_link"),
            ),
        )


# ---------------------------------------------------------------------------
# Per-city orchestration
# ---------------------------------------------------------------------------

def process_city(city_folder: Path, conn) -> None:
    city_slug = city_folder.name
    md_path = city_folder / f"{city_slug}.md"

    if not md_path.exists():
        print(f"  [SKIP] {city_folder.name}/ — no .md file found")
        return

    print(f"  Parsing {city_slug}.md ...")
    data = parse_city_md(city_folder)

    json_path = city_folder / f"{city_slug}.json"
    json_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  [OK] Written {json_path.name}")

    if conn is None:
        print(f"  [DB SKIP] No database connection -- JSON written only")
        return

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        city_id = upsert_city(cur, data)
        upsert_cost_breakdown(cur, city_id, data["cost_breakdown"])
        upsert_activities(cur, city_id, data["locations"])
    conn.commit()
    print(f"  [OK] DB upserted  city_id={city_id}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    target_slug = sys.argv[1] if len(sys.argv) > 1 else None

    conn = None
    if PSYCOPG2_AVAILABLE and DB_URL:
        try:
            conn = psycopg2.connect(DB_URL)
            print(f"Connected to PostgreSQL\n")
        except Exception as exc:
            print(f"DB connection failed: {exc}\nFalling back to JSON-only mode.\n")
    elif not DB_URL:
        print("DATABASE_URL not set — running in JSON-only mode.\n")

    city_folders = sorted(
        p for p in DATA_DIR.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )

    if target_slug:
        city_folders = [f for f in city_folders if f.name == target_slug]
        if not city_folders:
            print(f"City '{target_slug}' not found in {DATA_DIR}")
            sys.exit(1)

    for folder in city_folders:
        print(f"Processing: {folder.name}")
        try:
            process_city(folder, conn)
        except Exception as exc:
            print(f"  [ERROR] {exc}")
            if conn:
                conn.rollback()
        print()

    if conn:
        conn.close()

    print("Done.")


if __name__ == "__main__":
    main()
