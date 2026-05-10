from flask import Blueprint, g

from app.middleware.auth_middleware import require_auth
from app.services import budget_service, trip_service
from app.utils.helpers import make_response_envelope

budget_bp = Blueprint("budget", __name__, url_prefix="/api/v1/trips/<trip_slug>/budget")


@budget_bp.get("/")
@require_auth
def get_budget(trip_slug):
    trip = trip_service.get_trip(trip_slug, g.current_user)
    data = budget_service.compute_budget(trip)
    return make_response_envelope(data), 200
