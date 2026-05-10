from decimal import Decimal

from app.models import CityCostBreakdown, Stop, StopActivity, Trip


def compute_budget(trip: Trip) -> dict:
    stops = trip.stops.order_by(Stop.order_index).all()

    total_usd = Decimal("0")
    breakdown_by_category: dict[str, Decimal] = {
        "activities": Decimal("0"),
        "stay": Decimal("0"),
        "food": Decimal("0"),
        "transport": Decimal("0"),
    }
    breakdown_by_stop = []

    for stop in stops:
        days = (stop.departure_date - stop.arrival_date).days or 1
        city = stop.city

        # Activity costs from stop_activities
        activities_cost = Decimal("0")
        for sa in stop.activities.all():
            if sa.custom_cost_usd is not None:
                activities_cost += sa.custom_cost_usd
            elif sa.activity and sa.activity.cost_usd:
                activities_cost += sa.activity.cost_usd

        # City seeded cost estimates
        cb_map: dict[str, Decimal] = {}
        for cb in city.cost_breakdowns.all():
            cb_map[cb.expense_type.value] = cb.cost_usd

        estimated_stay = (cb_map.get("stay", Decimal("0")) * days)
        estimated_food = (cb_map.get("food", Decimal("0")) * days)
        estimated_local_transport = (cb_map.get("local_transport", Decimal("0")) * days)

        stop_total = activities_cost + estimated_stay + estimated_food + estimated_local_transport

        breakdown_by_category["activities"] += activities_cost
        breakdown_by_category["stay"] += estimated_stay
        breakdown_by_category["food"] += estimated_food
        breakdown_by_category["transport"] += estimated_local_transport
        total_usd += stop_total

        breakdown_by_stop.append(
            {
                "stop_id": str(stop.id),
                "city_name": city.name,
                "days": days,
                "subtotal_usd": float(stop_total),
                "activities_cost": float(activities_cost),
                "estimated_stay": float(estimated_stay),
                "estimated_food": float(estimated_food),
            }
        )

    total_days = (trip.end_date - trip.start_date).days or 1
    daily_avg = total_usd / total_days if total_days else Decimal("0")

    return {
        "total_usd": float(total_usd),
        "currency": "USD",
        "breakdown_by_category": {k: float(v) for k, v in breakdown_by_category.items()},
        "breakdown_by_stop": breakdown_by_stop,
        "daily_average_usd": float(daily_avg),
        "total_days": total_days,
        "over_budget_days": [],
    }
