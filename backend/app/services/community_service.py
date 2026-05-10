from app.extensions import db
from app.models import City, CommunityComment, CommunityLike, CommunityPost, Trip, User
from app.utils.errors import AppError
from app.utils.helpers import paginate_query


def list_posts(
    q: str | None,
    city_slug: str | None,
    user_id: str | None,
    sort: str,
    page: int,
    per_page: int,
    current_user_id: str,
):
    sort_col_map = {
        "created_at": CommunityPost.created_at.desc(),
        "likes_count": CommunityPost.likes_count.desc(),
    }
    order_clause = sort_col_map.get(sort, CommunityPost.created_at.desc())

    query = CommunityPost.query
    if q:
        query = query.filter(
            db.or_(
                CommunityPost.title.ilike(f"%{q}%"),
                CommunityPost.content.ilike(f"%{q}%"),
            )
        )
    if city_slug:
        city = City.query.filter_by(slug=city_slug).first()
        if city:
            query = query.filter_by(city_id=city.id)
    if user_id:
        query = query.filter_by(user_id=user_id)

    query = query.order_by(order_clause)
    return paginate_query(query, page, per_page)


def create_post(user: User, data: dict) -> CommunityPost:
    trip_id = None
    if data.get("trip_slug"):
        trip = Trip.query.filter_by(slug=data["trip_slug"], user_id=user.id).first()
        if trip:
            trip_id = trip.id

    city_id = None
    if data.get("city_slug"):
        city = City.query.filter_by(slug=data["city_slug"]).first()
        if city:
            city_id = city.id

    post = CommunityPost(
        user_id=user.id,
        trip_id=trip_id,
        city_id=city_id,
        title=data["title"],
        content=data["content"],
        image_urls=data.get("image_urls", []),
    )
    db.session.add(post)
    db.session.commit()
    return post


def get_post(post_id: str) -> CommunityPost:
    post = CommunityPost.query.get(post_id)
    if not post:
        raise AppError("Post not found", 404)
    return post


def update_post(post: CommunityPost, user: User, data: dict) -> CommunityPost:
    if str(post.user_id) != str(user.id):
        raise AppError("Access denied", 403)
    for key in ("title", "content", "image_urls"):
        if key in data:
            setattr(post, key, data[key])
    db.session.commit()
    return post


def delete_post(post: CommunityPost, user: User) -> None:
    if str(post.user_id) != str(user.id) and not user.is_admin:
        raise AppError("Access denied", 403)
    db.session.delete(post)
    db.session.commit()


def toggle_like(post: CommunityPost, user: User) -> tuple[bool, int]:
    existing = CommunityLike.query.filter_by(
        post_id=post.id, user_id=user.id
    ).first()
    if existing:
        db.session.delete(existing)
        post.likes_count = max(0, post.likes_count - 1)
        liked = False
    else:
        db.session.add(CommunityLike(post_id=post.id, user_id=user.id))
        post.likes_count += 1
        liked = True
    db.session.commit()
    return liked, post.likes_count


def get_comments(post: CommunityPost) -> list[CommunityComment]:
    return post.comments.order_by(CommunityComment.created_at.asc()).all()


def add_comment(post: CommunityPost, user: User, content: str) -> CommunityComment:
    comment = CommunityComment(
        post_id=post.id,
        user_id=user.id,
        content=content,
    )
    db.session.add(comment)
    post.comments_count += 1
    db.session.commit()
    return comment


def delete_comment(
    comment: CommunityComment, user: User
) -> None:
    if str(comment.user_id) != str(user.id) and not user.is_admin:
        raise AppError("Access denied", 403)
    post = comment.post
    db.session.delete(comment)
    post.comments_count = max(0, post.comments_count - 1)
    db.session.commit()
