from flask import Blueprint, g, request

from app.middleware.auth_middleware import require_auth
from app.schemas.trip_schema import (
    TripInputSchema,
    TripListOutputSchema,
    TripOutputSchema,
    TripUpdateSchema,
)
from app.services import trip_service
from app.utils.helpers import make_response_envelope, paginate_response
from webargs.flaskparser import use_args

trips_bp = Blueprint("trips", __name__, url_prefix="/api/v1/trips")


def _get_trip(slug: str):
    return trip_service.get_trip(slug, g.current_user)


@trips_bp.get("/")
@require_auth
def list_trips():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 50)
    sort = request.args.get("sort", "created_at")
    order = request.args.get("order", "desc")
    result = trip_service.list_trips(g.current_user, page, per_page, sort, order)
    return paginate_response(result, TripListOutputSchema(many=True)), 200


@trips_bp.post("/")
@require_auth
@use_args(TripInputSchema(), location="json")
def create_trip(args):
    trip = trip_service.create_trip(g.current_user, args)
    return make_response_envelope(TripOutputSchema().dump(trip)), 201


@trips_bp.get("/<slug>")
@require_auth
def get_trip(slug):
    trip = _get_trip(slug)
    return make_response_envelope(TripOutputSchema().dump(trip)), 200


@trips_bp.put("/<slug>")
@require_auth
@use_args(TripUpdateSchema(), location="json")
def update_trip(args, slug):
    trip = _get_trip(slug)
    trip = trip_service.update_trip(trip, args)
    return make_response_envelope(TripOutputSchema().dump(trip)), 200


@trips_bp.delete("/<slug>")
@require_auth
def delete_trip(slug):
    trip = _get_trip(slug)
    trip_service.delete_trip(trip)
    return "", 204


@trips_bp.post("/<slug>/share")
@require_auth
def enable_sharing(slug):
    trip = _get_trip(slug)
    token = trip_service.enable_sharing(trip)
    return make_response_envelope({
        "share_token": token,
        "share_url": f"https://traveloop.app/share/{token}",
    }), 200


@trips_bp.delete("/<slug>/share")
@require_auth
def disable_sharing(slug):
    trip = _get_trip(slug)
    trip_service.disable_sharing(trip)
    return make_response_envelope(None, "Sharing disabled"), 200


@trips_bp.get("/shared/<share_token>")
def get_shared_trip(share_token):
    trip = trip_service.get_trip_by_share_token(share_token)
    data = TripOutputSchema().dump(trip)
    data.pop("share_token", None)
    return make_response_envelope(data), 200
