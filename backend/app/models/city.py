import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from app.extensions import db
from app.models.enums import ExpenseTypeEnum


class City(db.Model):
    __tablename__ = "cities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug = Column(String(100), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    country_code = Column(String(2), nullable=True)
    region = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    cover_photo_url = Column(Text, nullable=True)
    map_link = Column(Text, nullable=True)
    best_time_months = Column(String(200), nullable=True)
    cost_index_usd = Column(Numeric(8, 2), nullable=False, default=0)
    popularity_score = Column(Integer, nullable=False, default=0)
    latitude = Column(Numeric(10, 6), nullable=True)
    longitude = Column(Numeric(10, 6), nullable=True)
    timezone = Column(String(60), nullable=True)
    iata_code = Column(String(3), nullable=True)
    wikipedia_title = Column(String(200), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    cost_breakdowns = db.relationship(
        "CityCostBreakdown",
        back_populates="city",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )
    activities = db.relationship(
        "Activity", back_populates="city", cascade="all, delete-orphan", lazy="dynamic"
    )
    stops = db.relationship("Stop", back_populates="city", lazy="dynamic")
    community_posts = db.relationship("CommunityPost", back_populates="city", lazy="dynamic")
    saved_by = db.relationship(
        "SavedCity", back_populates="city", cascade="all, delete-orphan", lazy="dynamic"
    )

    __table_args__ = (
        Index("cities_slug_idx", "slug", unique=True),
        Index("cities_name_idx", "name"),
        Index("cities_country_idx", "country"),
        Index("cities_country_code_idx", "country_code"),
        Index("cities_popularity_idx", "popularity_score"),
    )

    def __repr__(self) -> str:
        return f"<City {self.slug}>"


class CityCostBreakdown(db.Model):
    __tablename__ = "city_cost_breakdown"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False,
    )
    expense_type = Column(
        Enum(ExpenseTypeEnum, name="expense_type_enum"), nullable=False
    )
    cost_usd = Column(Numeric(8, 2), nullable=False)
    cost_local = Column(Numeric(10, 2), nullable=False)
    local_currency = Column(String(3), nullable=False)
    description = Column(Text, nullable=True)

    city = db.relationship("City", back_populates="cost_breakdowns")

    __table_args__ = (
        UniqueConstraint("city_id", "expense_type", name="uq_city_expense_type"),
    )
