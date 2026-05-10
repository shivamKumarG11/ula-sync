from flask import Blueprint, g, request

from app.middleware.auth_middleware import require_auth
from app.schemas.stop_schema import (
    ReorderStopsSchema,
    StopInputSchema,
    StopOutputSchema,
    StopUpdateSchema,
)
from app.services import stop_service, trip_service
from app.utils.helpers import make_response_envelope
from webargs.flaskparser import use_args

stops_bp = Blueprint("stops", __name__, url_prefix="/api/v1/trips/<trip_slug>/stops")


def _trip(trip_slug):
    return trip_service.get_trip(trip_slug, g.current_user)


@stops_bp.get("/")
@require_auth
def list_stops(trip_slug):
    trip = _trip(trip_slug)
    stops = stop_service.get_stops(trip)
    return make_response_envelope(StopOutputSchema(many=True).dump(stops)), 200


@stops_bp.post("/")
@require_auth
@use_args(StopInputSchema(), location="json")
def add_stop(args, trip_slug):
    trip = _trip(trip_slug)
    stop = stop_service.add_stop(trip, args)
    return make_response_envelope(StopOutputSchema().dump(stop)), 201


@stops_bp.put("/reorder")
@require_auth
@use_args(ReorderStopsSchema(), location="json")
def reorder_stops(args, trip_slug):
    trip = _trip(trip_slug)
    stops = stop_service.reorder_stops(trip, args["stop_ids"])
    return make_response_envelope(StopOutputSchema(many=True).dump(stops)), 200


@stops_bp.put("/<stop_id>")
@require_auth
@use_args(StopUpdateSchema(), location="json")
def update_stop(args, trip_slug, stop_id):
    trip = _trip(trip_slug)
    stop = stop_service.get_stop(stop_id, trip)
    stop = stop_service.update_stop(stop, args, trip)
    return make_response_envelope(StopOutputSchema().dump(stop)), 200


@stops_bp.delete("/<stop_id>")
@require_auth
def delete_stop(trip_slug, stop_id):
    trip = _trip(trip_slug)
    stop = stop_service.get_stop(stop_id, trip)
    stop_service.delete_stop(stop)
    return "", 204
