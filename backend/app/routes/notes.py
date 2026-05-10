from flask import Blueprint, g, request

from app.middleware.auth_middleware import require_auth
from app.schemas.note_schema import NoteInputSchema, NoteOutputSchema, NoteUpdateSchema
from app.services import note_service, trip_service
from app.utils.helpers import make_response_envelope, paginate_response
from webargs.flaskparser import use_args

notes_bp = Blueprint("notes", __name__, url_prefix="/api/v1/trips/<trip_slug>/notes")


def _trip(trip_slug):
    return trip_service.get_trip(trip_slug, g.current_user)


@notes_bp.get("/")
@require_auth
def list_notes(trip_slug):
    trip = _trip(trip_slug)
    stop_id = request.args.get("stop_id")
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    result = note_service.get_notes(trip, stop_id, page, per_page)
    return paginate_response(result, NoteOutputSchema(many=True)), 200


@notes_bp.post("/")
@require_auth
@use_args(NoteInputSchema(), location="json")
def create_note(args, trip_slug):
    trip = _trip(trip_slug)
    note = note_service.create_note(trip, args)
    return make_response_envelope(NoteOutputSchema().dump(note)), 201


@notes_bp.put("/<note_id>")
@require_auth
@use_args(NoteUpdateSchema(), location="json")
def update_note(args, trip_slug, note_id):
    trip = _trip(trip_slug)
    note = note_service.get_note(note_id, trip)
    note = note_service.update_note(note, args)
    return make_response_envelope(NoteOutputSchema().dump(note)), 200


@notes_bp.delete("/<note_id>")
@require_auth
def delete_note(trip_slug, note_id):
    trip = _trip(trip_slug)
    note = note_service.get_note(note_id, trip)
    note_service.delete_note(note)
    return "", 204
