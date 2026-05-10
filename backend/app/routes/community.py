from flask import Blueprint, g, request

from app.middleware.auth_middleware import require_auth
from app.schemas.community_schema import (
    CommentInputSchema,
    CommentOutputSchema,
    CommunityPostInputSchema,
    CommunityPostOutputSchema,
    CommunityPostUpdateSchema,
)
from app.services import community_service
from app.utils.helpers import make_response_envelope, paginate_response
from webargs.flaskparser import use_args

community_bp = Blueprint("community", __name__, url_prefix="/api/v1/community")


@community_bp.get("/")
@require_auth
def list_posts():
    result = community_service.list_posts(
        q=request.args.get("q"),
        city_slug=request.args.get("city_slug"),
        user_id=request.args.get("user_id"),
        sort=request.args.get("sort", "created_at"),
        page=request.args.get("page", 1, type=int),
        per_page=min(request.args.get("per_page", 20, type=int), 100),
        current_user_id=str(g.current_user.id),
    )
    return paginate_response(result, CommunityPostOutputSchema(many=True)), 200


@community_bp.post("/")
@require_auth
@use_args(CommunityPostInputSchema(), location="json")
def create_post(args):
    post = community_service.create_post(g.current_user, args)
    return make_response_envelope(CommunityPostOutputSchema().dump(post)), 201


@community_bp.get("/<post_id>")
@require_auth
def get_post(post_id):
    post = community_service.get_post(post_id)
    return make_response_envelope(CommunityPostOutputSchema().dump(post)), 200


@community_bp.put("/<post_id>")
@require_auth
@use_args(CommunityPostUpdateSchema(), location="json")
def update_post(args, post_id):
    post = community_service.get_post(post_id)
    post = community_service.update_post(post, g.current_user, args)
    return make_response_envelope(CommunityPostOutputSchema().dump(post)), 200


@community_bp.delete("/<post_id>")
@require_auth
def delete_post(post_id):
    post = community_service.get_post(post_id)
    community_service.delete_post(post, g.current_user)
    return "", 204


@community_bp.post("/<post_id>/like")
@require_auth
def toggle_like(post_id):
    post = community_service.get_post(post_id)
    liked, count = community_service.toggle_like(post, g.current_user)
    return make_response_envelope({"liked": liked, "likes_count": count}), 200


@community_bp.get("/<post_id>/comments")
@require_auth
def get_comments(post_id):
    post = community_service.get_post(post_id)
    comments = community_service.get_comments(post)
    return make_response_envelope(CommentOutputSchema(many=True).dump(comments)), 200


@community_bp.post("/<post_id>/comments")
@require_auth
@use_args(CommentInputSchema(), location="json")
def add_comment(args, post_id):
    post = community_service.get_post(post_id)
    comment = community_service.add_comment(post, g.current_user, args["content"])
    return make_response_envelope(CommentOutputSchema().dump(comment)), 201


@community_bp.delete("/<post_id>/comments/<comment_id>")
@require_auth
def delete_comment(post_id, comment_id):
    post = community_service.get_post(post_id)
    from app.models import CommunityComment
    from app.utils.errors import AppError
    comment = CommunityComment.query.filter_by(id=comment_id, post_id=post.id).first()
    if not comment:
        raise AppError("Comment not found", 404)
    community_service.delete_comment(comment, g.current_user)
    return "", 204
