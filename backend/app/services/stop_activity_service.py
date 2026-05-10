from datetime import date

from app.extensions import db
from app.models import Activity, City, Stop, StopActivity, Trip
from app.utils.errors import AppError


def add_stop_activity(stop: Stop, data: dict) -> StopActivity:
    return add_activity(stop, data)


def get_stop_activity(sa_id: str, stop: Stop) -> StopActivity:
    return get_activity_instance_by_id(sa_id, stop)


def update_stop_activity(sa: StopActivity, stop: Stop, data: dict) -> StopActivity:
    return update_activity(sa, data, stop)


def delete_stop_activity(sa: StopActivity) -> None:
    return delete_activity(sa)


def get_stop_activities(stop: Stop) -> list[StopActivity]:
    return (
        stop.activities.order_by(
            StopActivity.scheduled_date.asc().nullslast(),
            StopActivity.scheduled_time.asc().nullslast(),
        )
        .all()
    )


def add_activity(stop: Stop, data: dict) -> StopActivity:
    activity_id = data.get("activity_id")
    custom_name = data.get("custom_name")

    if not activity_id and not custom_name:
        raise AppError("Either activity_id or custom_name is required", 422)

    if activity_id:
        activity = Activity.query.get(str(activity_id))
        if not activity:
            raise AppError("Activity not found", 404)

    scheduled_date: date | None = data.get("scheduled_date")
    if scheduled_date:
        if not (stop.arrival_date <= scheduled_date <= stop.departure_date):
            raise AppError(
                f"scheduled_date must be within stop dates "
                f"({stop.arrival_date} – {stop.departure_date})",
                400,
            )

    sa = StopActivity(
        stop_id=stop.id,
        activity_id=str(activity_id) if activity_id else None,
        custom_name=custom_name,
        custom_cost_usd=data.get("custom_cost_usd"),
        category=data.get("category", "other"),
        scheduled_date=scheduled_date,
        scheduled_time=data.get("scheduled_time"),
        duration_hours=data.get("duration_hours"),
        notes=data.get("notes"),
    )
    db.session.add(sa)
    db.session.commit()
    return sa


def update_activity(sa: StopActivity, data: dict, stop: Stop) -> StopActivity:
    if "scheduled_date" in data and data["scheduled_date"]:
        sd: date = data["scheduled_date"]
        if not (stop.arrival_date <= sd <= stop.departure_date):
            raise AppError(
                f"scheduled_date must be within stop dates "
                f"({stop.arrival_date} – {stop.departure_date})",
                400,
            )

    for key in (
        "custom_name",
        "custom_cost_usd",
        "category",
        "scheduled_date",
        "scheduled_time",
        "duration_hours",
        "notes",
    ):
        if key in data:
            setattr(sa, key, data[key])

    db.session.commit()
    return sa


def delete_activity(sa: StopActivity) -> None:
    db.session.delete(sa)
    db.session.commit()


def get_activity_instance_by_id(sa_id: str, stop: Stop) -> StopActivity:
    sa = StopActivity.query.filter_by(id=sa_id, stop_id=stop.id).first()
    if not sa:
        raise AppError("Activity not found on this stop", 404)
    return sa
