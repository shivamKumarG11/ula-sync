"""
Seed script: Parse city markdown files → cities + activities + cost_breakdown rows.
Idempotent — uses upsert-style logic based on city slug.

Usage (from backend/ directory with venv active):
    python scripts/seed.py

Requirements:
    - .env loaded (for DATABASE_URL)
    - Flask app context
"""
import os
import re
import sys
import time

# Ensure project root on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.extensions import db
from app.models import Activity, City, CityCostBreakdown
from app.models.enums import ActivityCategoryEnum, ExpenseTypeEnum
from slugify import slugify

import requests

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

NOMINATIM_HEADERS = {
    "User-Agent": "Traveloop/1.0 (shivamkumargupta250904@gmail.com)"
}

# Map markdown expense types → enum values
_EXPENSE_MAP = {
    "travel": ExpenseTypeEnum.travel,
    "stay": ExpenseTypeEnum.stay,
    "food": ExpenseTypeEnum.food,
    "activities & entry tickets": ExpenseTypeEnum.activities,
    "activities": ExpenseTypeEnum.activities,
    "local transport": ExpenseTypeEnum.local_transport,
    "local transportation": ExpenseTypeEnum.local_transport,
}

# Map activity keywords → enum categories
_ACTIVITY_KEYWORDS = {
    ActivityCategoryEnum.sightseeing: ["fort", "palace", "temple", "monument", "heritage", "view", "sightseeing", "photography", "panoramic"],
    ActivityCategoryEnum.food: ["food", "restaurant", "street food", "cuisine", "eat", "meal", "culinary"],
    ActivityCategoryEnum.adventure: ["trek", "rafting", "adventure", "hiking", "kayak", "bungee", "zip", "climb", "river"],
    ActivityCategoryEnum.shopping: ["shopping", "market", "bazaar", "buy", "mall"],
    ActivityCategoryEnum.wellness: ["yoga", "spa", "meditation", "wellness", "ashram", "retreat"],
    ActivityCategoryEnum.cultural: ["cultural", "museum", "art", "dance", "music", "festival", "ceremony", "religion", "monastery"],
}


def _infer_category(text: str) -> ActivityCategoryEnum:
    text_lower = text.lower()
    for cat, keywords in _ACTIVITY_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return cat
    return ActivityCategoryEnum.other


def _geocode(city_name: str, country: str) -> tuple[float | None, float | None]:
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"city": city_name, "country": country, "format": "json", "limit": 1},
            headers=NOMINATIM_HEADERS,
            timeout=10,
        )
        data = resp.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as exc:
        print(f"  [geocode] Failed for {city_name}: {exc}")
    time.sleep(1)  # respect Nominatim rate limit
    return None, None


def _parse_cost_table(content: str) -> list[dict]:
    """Parse markdown cost table rows into dicts."""
    results = []
    in_table = False
    for line in content.splitlines():
        if "Expense Type" in line and "Average Cost" in line:
            in_table = True
            continue
        if in_table:
            if line.startswith("|---") or line.startswith("| ---"):
                continue
            if not line.startswith("|"):
                in_table = False
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 3:
                continue
            expense_type_raw = cells[0].lower().strip()
            cost_usd_raw = cells[1].strip().replace("$", "").replace(",", "").strip()
            local_currency_raw = cells[2].strip()

            expense_type = None
            for key, val in _EXPENSE_MAP.items():
                if key in expense_type_raw:
                    expense_type = val
                    break

            if not expense_type:
                continue

            try:
                cost_usd = float(cost_usd_raw) if cost_usd_raw and cost_usd_raw != "-" else 0.0
            except ValueError:
                cost_usd = 0.0

            # Extract local currency amount (e.g. "₹3,500" → 3500, "SGD 150" → 150)
            local_match = re.search(r"[\d,]+", local_currency_raw)
            cost_local = float(local_match.group().replace(",", "")) if local_match else 0.0

            # Extract currency symbol/code
            currency_match = re.match(r"([^\d\s,]+)", local_currency_raw)
            local_currency = currency_match.group(1) if currency_match else "USD"

            results.append({
                "expense_type": expense_type,
                "cost_usd": cost_usd,
                "cost_local": cost_local,
                "local_currency": local_currency,
            })
    return results


def _parse_activities(content: str, city_name: str) -> list[dict]:
    """Parse all location sections as activities."""
    activities = []
    # Match h2 location headers after "# Famous Locations"
    location_sections = re.split(r"\n## ", content)
    if len(location_sections) <= 1:
        return activities

    # Find index of "Famous Locations" marker
    famous_idx = None
    for i, section in enumerate(location_sections):
        if "Famous Locations" in section.split("\n")[0]:
            famous_idx = i
            break

    if famous_idx is None:
        return activities

    for section in location_sections[famous_idx + 1:]:
        lines = section.strip().splitlines()
        if not lines:
            continue
        name = lines[0].strip("# ").strip()
        if not name or len(name) < 3:
            continue

        # Description: lines after "### Description" before next ###
        description = ""
        desc_match = re.search(r"### Description\s*\n(.*?)(?=\n###|\Z)", section, re.DOTALL)
        if desc_match:
            description = desc_match.group(1).strip()

        # Map link
        map_link = None
        map_match = re.search(r"- (https://www\.google\.com/maps/[^\s\n]+)", section)
        if map_match:
            map_link = map_match.group(1)

        # Opening / closing times
        opening_time = None
        closing_time = None
        opening_match = re.search(r"Opening Time\s*\|\s*([^\n|]+)", section)
        closing_match = re.search(r"Closing Time\s*\|\s*([^\n|]+)", section)
        if opening_match:
            t = opening_match.group(1).strip()
            if t and "open" not in t.lower():
                opening_time = t
        if closing_match:
            t = closing_match.group(1).strip()
            if t and "open" not in t.lower():
                closing_time = t

        # Cost (foreign tourists as baseline)
        cost_usd = 0.0
        foreign_match = re.search(r"Foreign Tourists\s*\|\s*(₹|\\$|\$)?\s*([\d,]+)", section)
        if foreign_match:
            try:
                raw_cost = foreign_match.group(2).replace(",", "")
                inr_cost = float(raw_cost)
                # Convert ₹ to USD (approx)
                if "₹" in (foreign_match.group(1) or "") or inr_cost > 100:
                    cost_usd = round(inr_cost / 85.0, 2)
                else:
                    cost_usd = inr_cost
            except ValueError:
                pass

        # Duration
        duration_match = re.search(r"(\d+)[–-](\d+)\s*hours?", section)
        duration_hours = None
        if duration_match:
            duration_hours = (int(duration_match.group(1)) + int(duration_match.group(2))) / 2.0
        else:
            single_match = re.search(r"(\d+)\s*hours?", section)
            if single_match:
                duration_hours = float(single_match.group(1))

        # Booking required
        booking_required = bool(re.search(r"Mandatory|Recommended", section, re.IGNORECASE))
        booking_link_match = re.search(r"https?://(?!www\.google\.com/maps)[^\s\n]+", section)
        booking_link = booking_link_match.group(0) if booking_link_match else None

        category = _infer_category(name + " " + description)

        activities.append({
            "name": name,
            "description": description,
            "category": category,
            "cost_usd": cost_usd,
            "duration_hours": duration_hours or 2.0,
            "map_link": map_link,
            "opening_time": opening_time,
            "closing_time": closing_time,
            "booking_required": booking_required,
            "booking_link": booking_link,
        })

    return activities


def _extract_country_from_map_link(content: str) -> str | None:
    """Try to infer country from map link or description keywords."""
    # Common city-country mapping for our seeded cities
    return None


_CITY_META: dict[str, dict] = {
    "jaipur": {"country": "India", "country_code": "IN", "region": "Rajasthan", "timezone": "Asia/Kolkata", "iata_code": "JAI", "wikipedia_title": "Jaipur"},
    "rishikesh": {"country": "India", "country_code": "IN", "region": "Uttarakhand", "timezone": "Asia/Kolkata", "iata_code": "DED", "wikipedia_title": "Rishikesh"},
    "varanasi": {"country": "India", "country_code": "IN", "region": "Uttar Pradesh", "timezone": "Asia/Kolkata", "iata_code": "VNS", "wikipedia_title": "Varanasi"},
    "coimbatore": {"country": "India", "country_code": "IN", "region": "Tamil Nadu", "timezone": "Asia/Kolkata", "iata_code": "CJB", "wikipedia_title": "Coimbatore"},
    "hampi": {"country": "India", "country_code": "IN", "region": "Karnataka", "timezone": "Asia/Kolkata", "iata_code": "HBX", "wikipedia_title": "Hampi"},
    "nalanda": {"country": "India", "country_code": "IN", "region": "Bihar", "timezone": "Asia/Kolkata", "iata_code": "GAY", "wikipedia_title": "Nalanda"},
    "puducherry": {"country": "India", "country_code": "IN", "region": "Puducherry", "timezone": "Asia/Kolkata", "iata_code": "PNY", "wikipedia_title": "Pondicherry"},
    "shillong": {"country": "India", "country_code": "IN", "region": "Meghalaya", "timezone": "Asia/Kolkata", "iata_code": "SHL", "wikipedia_title": "Shillong"},
    "bali": {"country": "Indonesia", "country_code": "ID", "region": "Bali Province", "timezone": "Asia/Makassar", "iata_code": "DPS", "wikipedia_title": "Bali"},
    "dubai": {"country": "United Arab Emirates", "country_code": "AE", "region": "Dubai", "timezone": "Asia/Dubai", "iata_code": "DXB", "wikipedia_title": "Dubai"},
    "singapore": {"country": "Singapore", "country_code": "SG", "region": "Central Region", "timezone": "Asia/Singapore", "iata_code": "SIN", "wikipedia_title": "Singapore"},
    "kyoto": {"country": "Japan", "country_code": "JP", "region": "Kansai", "timezone": "Asia/Tokyo", "iata_code": "ITM", "wikipedia_title": "Kyoto"},
    "seoul": {"country": "South Korea", "country_code": "KR", "region": "Seoul Capital Area", "timezone": "Asia/Seoul", "iata_code": "ICN", "wikipedia_title": "Seoul"},
    "sydney": {"country": "Australia", "country_code": "AU", "region": "New South Wales", "timezone": "Australia/Sydney", "iata_code": "SYD", "wikipedia_title": "Sydney"},
    "cape-town": {"country": "South Africa", "country_code": "ZA", "region": "Western Cape", "timezone": "Africa/Johannesburg", "iata_code": "CPT", "wikipedia_title": "Cape Town"},
    "santorini": {"country": "Greece", "country_code": "GR", "region": "South Aegean", "timezone": "Europe/Athens", "iata_code": "JTR", "wikipedia_title": "Santorini"},
    "venice": {"country": "Italy", "country_code": "IT", "region": "Veneto", "timezone": "Europe/Rome", "iata_code": "VCE", "wikipedia_title": "Venice"},
    "rio-de-janerio": {"country": "Brazil", "country_code": "BR", "region": "Rio de Janeiro State", "timezone": "America/Sao_Paulo", "iata_code": "GIG", "wikipedia_title": "Rio de Janeiro"},
}


def seed_city(folder_name: str, md_path: str) -> None:
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # City name from first H1
    name_match = re.match(r"# (.+)", content)
    if not name_match:
        print(f"  [skip] No H1 in {md_path}")
        return

    city_name = name_match.group(1).strip()
    slug = slugify(city_name, separator="-", lowercase=True)

    meta = _CITY_META.get(folder_name) or _CITY_META.get(slug, {})
    country = meta.get("country", "Unknown")
    country_code = meta.get("country_code")
    region = meta.get("region")
    timezone = meta.get("timezone")
    iata_code = meta.get("iata_code")
    wikipedia_title = meta.get("wikipedia_title")

    # Description
    desc_match = re.search(r"## Description\s*\n(.*?)(?=\n---|\n##|\Z)", content, re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else ""

    # Map link
    map_link = None
    map_match = re.search(r"City Location:\s*(https?://[^\s\n]+)", content)
    if map_match:
        map_link = map_match.group(1).strip()

    # Best time
    best_time_match = re.search(r"Recommended Months:\s*([^\n]+)", content)
    best_time_months = best_time_match.group(1).strip() if best_time_match else None

    # Cost index (sum of all expense types)
    cost_rows = _parse_cost_table(content)
    cost_index_usd = sum(r["cost_usd"] for r in cost_rows) if cost_rows else None

    # Geocode
    print(f"  [geocode] {city_name}, {country} ...")
    lat, lon = _geocode(city_name, country)
    time.sleep(1)  # Nominatim rate limit

    # Upsert city
    city = City.query.filter_by(slug=slug).first()
    if city:
        print(f"  [update] {city_name} (slug={slug})")
    else:
        city = City(slug=slug)
        db.session.add(city)
        print(f"  [create] {city_name} (slug={slug})")

    city.name = city_name
    city.country = country
    city.country_code = country_code
    city.region = region
    city.description = description
    city.map_link = map_link
    city.best_time_months = best_time_months
    city.cost_index_usd = cost_index_usd
    city.popularity_score = 70  # default; can be updated manually
    city.latitude = lat
    city.longitude = lon
    city.timezone = timezone
    city.iata_code = iata_code
    city.wikipedia_title = wikipedia_title

    db.session.flush()

    # Upsert cost breakdown
    for row in cost_rows:
        breakdown = CityCostBreakdown.query.filter_by(
            city_id=city.id, expense_type=row["expense_type"]
        ).first()
        if not breakdown:
            breakdown = CityCostBreakdown(city_id=city.id, expense_type=row["expense_type"])
            db.session.add(breakdown)
        breakdown.cost_usd = row["cost_usd"]
        breakdown.cost_local = row["cost_local"]
        breakdown.local_currency = row["local_currency"]

    # Upsert activities
    activities = _parse_activities(content, city_name)
    existing_names = {
        a.name.lower() for a in Activity.query.filter_by(city_id=city.id).all()
    }
    new_count = 0
    for act_data in activities:
        if act_data["name"].lower() in existing_names:
            continue
        activity = Activity(
            city_id=city.id,
            name=act_data["name"],
            description=act_data["description"],
            category=act_data["category"],
            cost_usd=act_data["cost_usd"],
            duration_hours=act_data["duration_hours"],
            map_link=act_data["map_link"],
            opening_time=act_data["opening_time"],
            closing_time=act_data["closing_time"],
            booking_required=act_data["booking_required"],
            booking_link=act_data["booking_link"],
        )
        db.session.add(activity)
        new_count += 1

    db.session.commit()
    print(f"  [done] {city_name}: {len(cost_rows)} cost rows, {new_count} new activities")


def main():
    app = create_app()
    with app.app_context():
        if not os.path.isdir(DATA_DIR):
            print(f"Data directory not found: {DATA_DIR}")
            sys.exit(1)

        for folder in sorted(os.listdir(DATA_DIR)):
            folder_path = os.path.join(DATA_DIR, folder)
            if not os.path.isdir(folder_path):
                continue

            # Find the markdown file
            md_files = [f for f in os.listdir(folder_path) if f.endswith(".md")]
            if not md_files:
                print(f"[skip] No .md file in {folder}")
                continue

            md_path = os.path.join(folder_path, md_files[0])
            print(f"\n[seed] Processing: {folder}")
            try:
                seed_city(folder, md_path)
            except Exception as exc:
                print(f"  [error] {folder}: {exc}")
                db.session.rollback()

        print("\n[seed] Complete!")


if __name__ == "__main__":
    main()
