import re
import secrets
from datetime import datetime, timezone

from flask import current_app
from slugify import slugify

from app.extensions import bcrypt, db
from app.models import User
from app.utils.errors import AppError


def _generate_username(email: str) -> str:
    local = email.split("@")[0]
    base = slugify(local, max_length=30, word_boundary=True, separator="-")
    base = re.sub(r"-+", "-", base).strip("-") or "user"
    candidate = base[:30]
    n = 2
    while User.query.filter_by(username=candidate).first():
        suffix = f"-{n}"
        candidate = base[: 30 - len(suffix)] + suffix
        n += 1
    return candidate


def register_user(email: str, password: str, full_name: str) -> User:
    email = email.lower().strip()
    if User.query.filter_by(email=email).first():
        raise AppError("Email already registered", 409)

    username = _generate_username(email)
    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        email=email,
        username=username,
        password_hash=password_hash,
        full_name=full_name,
    )
    db.session.add(user)
    db.session.commit()
    return user


def login_user(email: str, password: str) -> User:
    email = email.lower().strip()
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        raise AppError("Invalid credentials", 401)
    return user


def get_user_by_id(user_id: str) -> User:
    user = User.query.get(user_id)
    if not user:
        raise AppError("User not found", 404)
    return user


def update_user_profile(user: User, data: dict) -> User:
    allowed = {
        "full_name", "bio", "job_title", "company", "home_city", "home_country",
        "date_of_birth", "interests", "travel_style", "language_preference",
        "preferred_currency", "profile_photo_url", "onboarding_completed",
        "phone_number",
    }
    for key, value in data.items():
        if key in allowed:
            setattr(user, key, value)
    db.session.commit()
    return user


def delete_user(user: User) -> None:
    db.session.delete(user)
    db.session.commit()
