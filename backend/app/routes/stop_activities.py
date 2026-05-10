from flask import Blueprint, g

from app.middleware.auth_middleware import require_auth
from app.schemas.activity_schema import (
    StopActivityInputSchema,
    StopActivityOutputSchema,
    StopActivityUpdateSchema,
)
from app.services import stop_activity_service, stop_service, trip_service
from app.utils.helpers import make_response_envelope
from webargs.flaskparser import use_args

stop_activities_bp = Blueprint(
    "stop_activities",
    __name__,
    url_prefix="/api/v1/trips/<trip_slug>/stops/<stop_id>/activities",
)


def _stop(trip_slug, stop_id):
    trip = trip_service.get_trip(trip_slug, g.current_user)
    return stop_service.get_stop(stop_id, trip)


@stop_activities_bp.get("/")
@require_auth
def list_activities(trip_slug, stop_id):
    stop = _stop(trip_slug, stop_id)
    activities = stop_activity_service.get_stop_activities(stop)
    return make_response_envelope(StopActivityOutputSchema(many=True).dump(activities)), 200


@stop_activities_bp.post("/")
@require_auth
@use_args(StopActivityInputSchema(), location="json")
def add_activity(args, trip_slug, stop_id):
    stop = _stop(trip_slug, stop_id)
    sa = stop_activity_service.add_stop_activity(stop, args)
    return make_response_envelope(StopActivityOutputSchema().dump(sa)), 201


@stop_activities_bp.put("/<activity_id>")
@require_auth
@use_args(StopActivityUpdateSchema(), location="json")
def update_activity(args, trip_slug, stop_id, activity_id):
    stop = _stop(trip_slug, stop_id)
    sa = stop_activity_service.get_stop_activity(activity_id, stop)
    sa = stop_activity_service.update_stop_activity(sa, stop, args)
    return make_response_envelope(StopActivityOutputSchema().dump(sa)), 200


@stop_activities_bp.delete("/<activity_id>")
@require_auth
def delete_activity(trip_slug, stop_id, activity_id):
    stop = _stop(trip_slug, stop_id)
    sa = stop_activity_service.get_stop_activity(activity_id, stop)
    stop_activity_service.delete_stop_activity(sa)
    return "", 204
