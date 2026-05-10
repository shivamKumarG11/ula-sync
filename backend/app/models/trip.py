import enum
import uuid

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import JSON, Uuid as UUID

from app.extensions import db
from app.models.mixins import TimestampMixin


class Trip(TimestampMixin, db.Model):
    __tablename__ = "trips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    slug = Column(String(230), nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    cover_photo_url = Column(Text, nullable=True)
    is_public = Column(Boolean, nullable=False, default=False)
    share_token = Column(String(64), unique=True, nullable=True)
    checklist_share_token = Column(String(64), unique=True, nullable=True)

    user = db.relationship("User", back_populates="trips")
    stops = db.relationship(
        "Stop", back_populates="trip", cascade="all, delete-orphan",
        order_by="Stop.order_index", lazy="dynamic"
    )
    notes = db.relationship("TripNote", back_populates="trip", cascade="all, delete-orphan", lazy="dynamic")
    packing_items = db.relationship("PackingItem", back_populates="trip", cascade="all, delete-orphan", lazy="dynamic")
    invoice = db.relationship("Invoice", back_populates="trip", uselist=False, cascade="all, delete-orphan")
    community_posts = db.relationship("CommunityPost", back_populates="trip", lazy="dynamic")

    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="trip_end_after_start"),
        Index("trips_user_id_idx", "user_id"),
        Index("trips_user_start_date_idx", "user_id", "start_date"),
        Index("trips_slug_idx", "slug", unique=True),
        Index("trips_share_token_idx", "share_token", unique=True),
        Index("trips_checklist_token_idx", "checklist_share_token", unique=True),
    )

    def __repr__(self) -> str:
        return f"<Trip {self.slug}>"
