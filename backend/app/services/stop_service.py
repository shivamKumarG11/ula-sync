from datetime import date

from app.extensions import db
from app.models import City, Stop, Trip
from app.utils.errors import AppError
from app.utils.validators import validate_date_within_range


def _assert_dates_within_trip(
    arrival: date, departure: date, trip: Trip
) -> None:
    if arrival < trip.start_date or departure > trip.end_date:
        raise AppError(
            f"Stop dates ({arrival} – {departure}) must be within "
            f"trip dates ({trip.start_date} – {trip.end_date})",
            400,
        )


def get_stops(trip: Trip) -> list[Stop]:
    return trip.stops.order_by(Stop.order_index).all()


def add_stop(trip: Trip, data: dict) -> Stop:
    city = City.query.get(data["city_id"])
    if not city:
        raise AppError("City not found", 404)

    arrival: date = data["arrival_date"]
    departure: date = data["departure_date"]
    _assert_dates_within_trip(arrival, departure, trip)

    # Assign order_index
    order_index = data.get("order_index")
    if order_index is None:
        max_order = db.session.query(db.func.max(Stop.order_index)).filter_by(
            trip_id=trip.id
        ).scalar()
        order_index = (max_order or -1) + 1

    stop = Stop(
        trip_id=trip.id,
        city_id=city.id,
        order_index=order_index,
        arrival_date=arrival,
        departure_date=departure,
        notes=data.get("notes"),
    )
    db.session.add(stop)
    db.session.commit()
    return stop


def update_stop(stop: Stop, data: dict, trip: Trip) -> Stop:
    arrival = data.get("arrival_date", stop.arrival_date)
    departure = data.get("departure_date", stop.departure_date)
    _assert_dates_within_trip(arrival, departure, trip)

    for key in ("arrival_date", "departure_date", "notes"):
        if key in data:
            setattr(stop, key, data[key])
    db.session.commit()
    return stop


def delete_stop(stop: Stop) -> None:
    db.session.delete(stop)
    db.session.commit()


def reorder_stops(trip: Trip, stop_ids: list) -> list[Stop]:
    stops = Stop.query.filter_by(trip_id=trip.id).all()
    db_ids = {str(s.id) for s in stops}
    input_ids = [str(sid) for sid in stop_ids]

    if set(input_ids) != db_ids:
        raise AppError("stop_ids must contain exactly all stops for this trip", 400)

    id_to_stop = {str(s.id): s for s in stops}
    for idx, sid in enumerate(input_ids):
        id_to_stop[sid].order_index = idx

    db.session.commit()
    return sorted(stops, key=lambda s: s.order_index)
