from flask import Blueprint, g, request

from app.extensions import limiter
from app.middleware.auth_middleware import require_auth
from app.schemas.ai_schema import (
    ChatInputSchema as AIChatInputSchema,
    GenerateItineraryInputSchema as AIGenerateItineraryInputSchema,
    PackingAdviceInputSchema as AIPackingAdviceInputSchema,
    RecommendTransportInputSchema as AIRecommendTransportInputSchema,
    ReviewTripInputSchema as AIReviewTripInputSchema,
    SuggestActivitiesInputSchema as AISuggestActivitiesInputSchema,
)
from app.services import ai_service
from app.utils.helpers import make_response_envelope
from webargs.flaskparser import use_args

ai_bp = Blueprint("ai", __name__, url_prefix="/api/v1/ai")


@ai_bp.post("/generate-itinerary")
@require_auth
@limiter.limit("3 per minute", key_func=lambda: str(g.current_user.id))
@use_args(AIGenerateItineraryInputSchema(), location="json")
def generate_itinerary(args):
    result = ai_service.generate_itinerary(
        g.current_user, args["trip_slug"], args.get("preferences", {})
    )
    return make_response_envelope(result), 200


@ai_bp.post("/suggest-activities")
@require_auth
@limiter.limit("10 per minute", key_func=lambda: str(g.current_user.id))
@use_args(AISuggestActivitiesInputSchema(), location="json")
def suggest_activities(args):
    result = ai_service.suggest_activities(g.current_user, args)
    return make_response_envelope(result), 200


@ai_bp.post("/recommend-transport")
@require_auth
@limiter.limit("5 per minute", key_func=lambda: str(g.current_user.id))
@use_args(AIRecommendTransportInputSchema(), location="json")
def recommend_transport(args):
    result = ai_service.recommend_transport(g.current_user, args)
    return make_response_envelope(result), 200


@ai_bp.post("/review-trip")
@require_auth
@limiter.limit("3 per minute", key_func=lambda: str(g.current_user.id))
@use_args(AIReviewTripInputSchema(), location="json")
def review_trip(args):
    result = ai_service.review_trip(g.current_user, args["trip_slug"])
    return make_response_envelope(result), 200


@ai_bp.post("/packing-advice")
@require_auth
@limiter.limit("5 per minute", key_func=lambda: str(g.current_user.id))
@use_args(AIPackingAdviceInputSchema(), location="json")
def packing_advice(args):
    result = ai_service.packing_advice(
        g.current_user, args["trip_slug"], args.get("existing_item_names", [])
    )
    return make_response_envelope(result), 200


@ai_bp.post("/chat")
@require_auth
@limiter.limit("20 per minute", key_func=lambda: str(g.current_user.id))
@use_args(AIChatInputSchema(), location="json")
def chat(args):
    result = ai_service.chat(
        g.current_user, args["messages"], args.get("context")
    )
    return make_response_envelope(result), 200
