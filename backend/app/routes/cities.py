from flask import Blueprint, request

from app.middleware.auth_middleware import optional_auth
from app.schemas.city_schema import CityListOutputSchema, CityOutputSchema
from app.services import city_service
from app.utils.helpers import make_response_envelope, paginate_response

cities_bp = Blueprint("cities", __name__, url_prefix="/api/v1/cities")


@cities_bp.get("/")
@optional_auth
def list_cities():
    q = request.args.get("q")
    country = request.args.get("country")
    country_code = request.args.get("country_code")
    region = request.args.get("region")
    sort = request.args.get("sort", "popularity_score")
    order = request.args.get("order", "desc")
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)

    result = city_service.search_cities(
        q=q, country=country, country_code=country_code,
        region=region, sort=sort, order=order, page=page, per_page=per_page
    )
    return paginate_response(result, CityListOutputSchema(many=True)), 200


@cities_bp.get("/<slug>")
@optional_auth
def get_city(slug):
    city = city_service.get_city_by_slug(slug)
    return make_response_envelope(CityOutputSchema().dump(city)), 200
