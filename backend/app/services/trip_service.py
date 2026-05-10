import secrets
from datetime import date

from slugify import slugify

from app.extensions import db
from app.models import Stop, Trip, User
from app.utils.errors import AppError


def _generate_slug(name: str, trip_id) -> str:
    base = slugify(name, max_length=220, word_boundary=True, separator="-")
    return f"{base}-{str(trip_id)[:8]}"


def create_trip(user: User, data: dict) -> Trip:
    start: date = data["start_date"]
    end: date = data["end_date"]
    if end < start:
        raise AppError("end_date must be >= start_date", 400)

    trip = Trip(
        user_id=user.id,
        name=data["name"],
        description=data.get("description"),
        start_date=start,
        end_date=end,
        cover_photo_url=data.get("cover_photo_url"),
    )
    db.session.add(trip)
    db.session.flush()  # get ID before slug generation
    trip.slug = _generate_slug(trip.name, trip.id)
    db.session.commit()
    return trip


def get_trips_for_user(user: User, page: int, per_page: int, sort: str, order: str):
    from app.utils.helpers import paginate_query

    sort_col_map = {
        "created_at": Trip.created_at,
        "start_date": Trip.start_date,
        "name": Trip.name,
    }
    col = sort_col_map.get(sort, Trip.created_at)
    col = col.desc() if order == "desc" else col.asc()

    q = Trip.query.filter_by(user_id=user.id).order_by(col)
    return paginate_query(q, page, per_page)


def get_trip_by_slug(slug: str, user_id) -> Trip:
    trip = Trip.query.filter_by(slug=slug).first()
    if not trip:
        raise AppError("Trip not found", 404)
    if str(trip.user_id) != str(user_id):
        raise AppError("Access denied", 403)
    return trip


def get_public_trip(share_token: str) -> Trip:
    trip = Trip.query.filter_by(share_token=share_token, is_public=True).first()
    if not trip:
        raise AppError("Shared trip not found", 404)
    return trip


def update_trip(trip: Trip, data: dict) -> Trip:
    start = data.get("start_date", trip.start_date)
    end = data.get("end_date", trip.end_date)
    if end < start:
        raise AppError("end_date must be >= start_date", 400)

    name_changed = "name" in data and data["name"] != trip.name

    for key in ("name", "description", "start_date", "end_date", "cover_photo_url", "is_public"):
        if key in data:
            setattr(trip, key, data[key])

    if name_changed:
        trip.slug = _generate_slug(trip.name, trip.id)

    db.session.commit()
    return trip


def delete_trip(trip: Trip) -> None:
    db.session.delete(trip)
    db.session.commit()


def enable_sharing(trip: Trip) -> Trip:
    if not trip.share_token:
        trip.share_token = secrets.token_urlsafe(32)
    trip.is_public = True
    db.session.commit()
    return trip


def disable_sharing(trip: Trip) -> Trip:
    trip.is_public = False
    trip.share_token = None
    db.session.commit()
    return trip
