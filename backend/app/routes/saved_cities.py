from flask import Blueprint, g, request

from app.middleware.auth_middleware import require_auth
from app.schemas.city_schema import CityListOutputSchema
from app.services import saved_city_service
from app.utils.errors import AppError
from app.utils.helpers import make_response_envelope
from webargs.flaskparser import use_args
from marshmallow import Schema, fields, validate

saved_cities_bp = Blueprint("saved_cities", __name__, url_prefix="/api/v1/users/me/saved")


class _SaveCitySchema(Schema):
    city_id = fields.UUID(required=True)


@saved_cities_bp.get("/")
@require_auth
def list_saved():
    rows = saved_city_service.get_saved_cities(g.current_user)
    from app.schemas.city_schema import CityListOutputSchema as Schema
    cities = [city for _, city in rows]
    return make_response_envelope(Schema(many=True).dump(cities)), 200


@saved_cities_bp.post("/")
@require_auth
@use_args(_SaveCitySchema(), location="json")
def save_city(args):
    saved_city_service.save_city(g.current_user, str(args["city_id"]))
    return make_response_envelope({"city_id": str(args["city_id"])}, "City saved"), 201


@saved_cities_bp.delete("/<city_id>")
@require_auth
def unsave_city(city_id):
    saved_city_service.unsave_city(g.current_user, city_id)
    return "", 204
