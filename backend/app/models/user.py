import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    Enum,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.extensions import db
from app.models.enums import TravelStyleEnum
from app.models.mixins import TimestampMixin


class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(30), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    home_city = Column(String(100), nullable=True)
    home_country = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    job_title = Column(String(100), nullable=True)
    company = Column(String(100), nullable=True)
    interests = Column(JSONB, nullable=False, default=list)
    travel_style = Column(
        Enum(TravelStyleEnum, name="travel_style_enum"), nullable=True
    )
    date_of_birth = Column(Date, nullable=True)
    profile_photo_url = Column(Text, nullable=True)
    language_preference = Column(String(10), nullable=False, default="en")
    preferred_currency = Column(String(3), nullable=False, default="USD")
    is_admin = Column(Boolean, nullable=False, default=False)
    onboarding_completed = Column(Boolean, nullable=False, default=False)

    trips = db.relationship(
        "Trip", back_populates="user", cascade="all, delete-orphan", lazy="dynamic"
    )
    community_posts = db.relationship(
        "CommunityPost", back_populates="user", cascade="all, delete-orphan", lazy="dynamic"
    )
    saved_cities = db.relationship(
        "SavedCity", back_populates="user", cascade="all, delete-orphan", lazy="dynamic"
    )

    __table_args__ = (
        Index("users_email_idx", "email", unique=True),
        Index("users_username_idx", "username", unique=True),
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"
