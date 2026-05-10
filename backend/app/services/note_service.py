from app.extensions import db
from app.models import Stop, Trip, TripNote
from app.utils.errors import AppError
from app.utils.helpers import paginate_query


def get_notes(trip: Trip, stop_id: str | None, page: int, per_page: int):
    q = TripNote.query.filter_by(trip_id=trip.id)
    if stop_id:
        q = q.filter_by(stop_id=stop_id)
    q = q.order_by(TripNote.created_at.desc())
    return paginate_query(q, page, per_page)


def create_note(trip: Trip, data: dict) -> TripNote:
    stop_id = data.get("stop_id")
    if stop_id:
        stop = Stop.query.filter_by(id=str(stop_id), trip_id=trip.id).first()
        if not stop:
            raise AppError("Stop not found on this trip", 404)

    note = TripNote(
        trip_id=trip.id,
        stop_id=str(stop_id) if stop_id else None,
        title=data["title"],
        content=data["content"],
    )
    db.session.add(note)
    db.session.commit()
    return note


def get_note(note_id: str, trip: Trip) -> TripNote:
    note = TripNote.query.filter_by(id=note_id, trip_id=trip.id).first()
    if not note:
        raise AppError("Note not found", 404)
    return note


def update_note(note: TripNote, data: dict) -> TripNote:
    for key in ("title", "content"):
        if key in data:
            setattr(note, key, data[key])
    db.session.commit()
    return note


def delete_note(note: TripNote) -> None:
    db.session.delete(note)
    db.session.commit()
