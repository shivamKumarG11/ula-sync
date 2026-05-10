from functools import wraps

from flask import g
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.models import User
from app.utils.errors import AppError


def _current_user() -> User:
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        raise AppError("User not found", 401)
    return user


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request(locations=["cookies"])
        g.current_user = _current_user()
        return fn(*args, **kwargs)
    return wrapper


def require_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request(locations=["cookies"])
        user = _current_user()
        if not user.is_admin:
            raise AppError("Admin access required", 403)
        g.current_user = user
        return fn(*args, **kwargs)
    return wrapper


def optional_auth(fn):
    """Sets g.current_user if a valid token is present, otherwise None."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(locations=["cookies"], optional=True)
            user_id = get_jwt_identity()
            g.current_user = User.query.get(user_id) if user_id else None
        except Exception:
            g.current_user = None
        return fn(*args, **kwargs)
    return wrapper
