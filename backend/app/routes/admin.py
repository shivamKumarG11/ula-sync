from flask import Blueprint, g, request

from app.middleware.auth_middleware import require_auth
from app.schemas.city_schema import CityListOutputSchema
from app.schemas.user_schema import UserMinimalOutputSchema
from app.services import admin_service
from app.utils.helpers import make_response_envelope, paginate_response
from app.utils.errors import AppError

admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1/admin")


def _require_admin():
    if not g.current_user.is_admin:
        raise AppError("Admin access required", 403)


@admin_bp.get("/stats")
@require_auth
def get_stats():
    _require_admin()
    return make_response_envelope(admin_service.get_stats()), 200


@admin_bp.get("/users")
@require_auth
def list_users():
    _require_admin()
    result = admin_service.list_users(
        q=request.args.get("q"),
        page=request.args.get("page", 1, type=int),
        per_page=min(request.args.get("per_page", 20, type=int), 100),
    )
    return paginate_response(result, UserMinimalOutputSchema(many=True)), 200


@admin_bp.delete("/users/<user_id>")
@require_auth
def delete_user(user_id):
    _require_admin()
    if str(g.current_user.id) == user_id:
        raise AppError("Cannot delete your own account", 400)
    admin_service.delete_user(user_id)
    return "", 204


@admin_bp.put("/users/<user_id>/admin")
@require_auth
def set_admin(user_id):
    _require_admin()
    is_admin = request.get_json(silent=True, force=True) or {}
    user = admin_service.set_admin(user_id, bool(is_admin.get("is_admin", True)))
    return make_response_envelope(UserMinimalOutputSchema().dump(user)), 200


@admin_bp.get("/cities")
@require_auth
def list_cities():
    _require_admin()
    from app.services import city_service
    result = city_service.search_cities(
        q=request.args.get("q"),
        country=None,
        country_code=None,
        region=None,
        sort="popularity_score",
        order="desc",
        page=request.args.get("page", 1, type=int),
        per_page=min(request.args.get("per_page", 20, type=int), 100),
    )
    return paginate_response(result, CityListOutputSchema(many=True)), 200


@admin_bp.get("/trips")
@require_auth
def list_trips():
    _require_admin()
    result = admin_service.list_trips(
        page=request.args.get("page", 1, type=int),
        per_page=min(request.args.get("per_page", 20, type=int), 100),
    )
    from app.schemas.trip_schema import TripListOutputSchema
    return paginate_response(result, TripListOutputSchema(many=True)), 200


@admin_bp.delete("/trips/<trip_id>")
@require_auth
def delete_trip(trip_id):
    _require_admin()
    admin_service.delete_trip(trip_id)
    return "", 204


@admin_bp.get("/community")
@require_auth
def list_posts():
    _require_admin()
    result = admin_service.list_community_posts(
        page=request.args.get("page", 1, type=int),
        per_page=min(request.args.get("per_page", 20, type=int), 100),
    )
    from app.schemas.community_schema import CommunityPostOutputSchema
    return paginate_response(result, CommunityPostOutputSchema(many=True)), 200


@admin_bp.delete("/community/<post_id>")
@require_auth
def delete_post(post_id):
    _require_admin()
    admin_service.delete_community_post(post_id)
    return "", 204
