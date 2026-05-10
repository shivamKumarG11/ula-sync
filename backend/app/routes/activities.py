from flask import Blueprint, request

from app.middleware.auth_middleware import require_auth
from app.schemas.activity_schema import ActivityOutputSchema
from app.services import city_service
from app.utils.helpers import make_response_envelope, paginate_response

activities_bp = Blueprint("activities", __name__, url_prefix="/api/v1/cities/<city_slug>/activities")


@activities_bp.get("/")
@require_auth
def search_activities(city_slug):
    city = city_service.get_city_by_slug(city_slug)
    result = city_service.search_activities(
        city=city,
        q=request.args.get("q"),
        category=request.args.get("category"),
        min_cost=request.args.get("min_cost", type=float),
        max_cost=request.args.get("max_cost", type=float),
        max_duration=request.args.get("max_duration", type=float),
        booking_required=request.args.get("booking_required", type=lambda v: v.lower() == "true")
            if request.args.get("booking_required") else None,
        page=request.args.get("page", 1, type=int),
        per_page=min(request.args.get("per_page", 20, type=int), 100),
    )
    return paginate_response(result, ActivityOutputSchema(many=True)), 200


@activities_bp.get("/<activity_id>")
@require_auth
def get_activity(city_slug, activity_id):
    city_service.get_city_by_slug(city_slug)  # validate city exists
    activity = city_service.get_activity_by_id(activity_id)
    return make_response_envelope(ActivityOutputSchema().dump(activity)), 200
