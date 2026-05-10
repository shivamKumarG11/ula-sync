from datetime import datetime, timedelta, timezone

from sqlalchemy import func

from app.extensions import db
from app.models import City, CommunityPost, Trip, User
from app.utils.errors import AppError


def get_stats() -> dict:
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)

    total_users = db.session.query(func.count(User.id)).scalar()
    new_users_30d = (
        db.session.query(func.count(User.id))
        .filter(User.created_at >= thirty_days_ago)
        .scalar()
    )
    total_trips = db.session.query(func.count(Trip.id)).scalar()
    public_trips = db.session.query(func.count(Trip.id)).filter(Trip.is_public.is_(True)).scalar()
    total_cities = db.session.query(func.count(City.id)).scalar()
    total_posts = db.session.query(func.count(CommunityPost.id)).scalar()

    return {
        "users": {
            "total": total_users,
            "new_last_30_days": new_users_30d,
        },
        "trips": {
            "total": total_trips,
            "public": public_trips,
        },
        "content": {
            "cities": total_cities,
            "community_posts": total_posts,
        },
    }


def list_users(q: str | None, page: int, per_page: int) -> dict:
    from app.utils.helpers import paginate_query

    query = User.query.order_by(User.created_at.desc())
    if q:
        query = query.filter(
            db.or_(
                User.email.ilike(f"%{q}%"),
                User.username.ilike(f"%{q}%"),
                User.full_name.ilike(f"%{q}%"),
            )
        )
    return paginate_query(query, page, per_page)


def get_user(user_id: str) -> User:
    user = User.query.get(user_id)
    if not user:
        raise AppError("User not found", 404)
    return user


def set_admin(user_id: str, is_admin: bool) -> User:
    user = get_user(user_id)
    user.is_admin = is_admin
    db.session.commit()
    return user


def delete_user(user_id: str) -> None:
    user = get_user(user_id)
    db.session.delete(user)
    db.session.commit()


def list_trips(page: int, per_page: int) -> dict:
    from app.utils.helpers import paginate_query

    query = Trip.query.order_by(Trip.created_at.desc())
    return paginate_query(query, page, per_page)


def delete_trip(trip_id: str) -> None:
    trip = Trip.query.get(trip_id)
    if not trip:
        raise AppError("Trip not found", 404)
    db.session.delete(trip)
    db.session.commit()


def list_community_posts(page: int, per_page: int) -> dict:
    from app.utils.helpers import paginate_query

    query = CommunityPost.query.order_by(CommunityPost.created_at.desc())
    return paginate_query(query, page, per_page)


def delete_community_post(post_id: str) -> None:
    post = CommunityPost.query.get(post_id)
    if not post:
        raise AppError("Post not found", 404)
    db.session.delete(post)
    db.session.commit()
