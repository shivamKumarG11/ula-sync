from flask import Blueprint, g

from app.middleware.auth_middleware import require_auth
from app.schemas.packing_schema import PackingItemInputSchema, PackingItemOutputSchema, PackingItemUpdateSchema
from app.services import packing_service, trip_service
from app.utils.helpers import make_response_envelope
from webargs.flaskparser import use_args

packing_bp = Blueprint("packing", __name__, url_prefix="/api/v1/trips/<trip_slug>/packing")


def _trip(trip_slug):
    return trip_service.get_trip(trip_slug, g.current_user)


@packing_bp.get("/")
@require_auth
def list_items(trip_slug):
    trip = _trip(trip_slug)
    grouped = packing_service.get_packing_items(trip)
    serialized = {
        cat: PackingItemOutputSchema(many=True).dump(items)
        for cat, items in grouped.items()
    }
    return make_response_envelope(serialized), 200


@packing_bp.post("/")
@require_auth
@use_args(PackingItemInputSchema(), location="json")
def add_item(args, trip_slug):
    trip = _trip(trip_slug)
    item = packing_service.add_item(trip, args)
    return make_response_envelope(PackingItemOutputSchema().dump(item)), 201


@packing_bp.post("/batch")
@require_auth
def add_items_batch(trip_slug):
    from flask import request
    trip = _trip(trip_slug)
    items_data = request.get_json() or []
    items = packing_service.add_items_batch(trip, items_data)
    return make_response_envelope(PackingItemOutputSchema(many=True).dump(items)), 201


@packing_bp.put("/<item_id>")
@require_auth
@use_args(PackingItemUpdateSchema(), location="json")
def update_item(args, trip_slug, item_id):
    trip = _trip(trip_slug)
    item = packing_service.get_item(item_id, trip)
    item = packing_service.update_item(item, args)
    return make_response_envelope(PackingItemOutputSchema().dump(item)), 200


@packing_bp.delete("/<item_id>")
@require_auth
def delete_item(trip_slug, item_id):
    trip = _trip(trip_slug)
    item = packing_service.get_item(item_id, trip)
    packing_service.delete_item(item)
    return "", 204


@packing_bp.post("/seed")
@require_auth
def seed_items(trip_slug):
    trip = _trip(trip_slug)
    added = packing_service.seed_default_items(trip)
    return make_response_envelope({"added": added}, f"{added} items added"), 200


@packing_bp.post("/reset")
@require_auth
def reset_checklist(trip_slug):
    trip = _trip(trip_slug)
    packing_service.reset_checklist(trip)
    return make_response_envelope(None, "Checklist reset"), 200


@packing_bp.get("/share-token")
@require_auth
def get_share_token(trip_slug):
    trip = _trip(trip_slug)
    token = packing_service.generate_checklist_share_token(trip)
    return make_response_envelope({"token": token}), 200
