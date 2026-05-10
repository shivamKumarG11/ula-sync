import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    Time,
)
from sqlalchemy import DateTime, Uuid as UUID

from app.extensions import db
from app.models.enums import ActivityCategoryEnum


class Activity(db.Model):
    __tablename__ = "activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=True,
    )
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(
        Enum(ActivityCategoryEnum, name="activity_category_enum"), nullable=False
    )
    cost_usd = Column(Numeric(8, 2), nullable=False, default=0)
    duration_hours = Column(Numeric(4, 1), nullable=True)
    image_url = Column(Text, nullable=True)
    map_link = Column(Text, nullable=True)
    opening_time = Column(Time, nullable=True)
    closing_time = Column(Time, nullable=True)
    booking_required = Column(Boolean, nullable=False, default=False)
    booking_link = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    city = db.relationship("City", back_populates="activities")
    stop_activities = db.relationship("StopActivity", back_populates="activity", lazy="dynamic")

    __table_args__ = (
        Index("activities_city_id_idx", "city_id"),
        Index("activities_category_idx", "category"),
    )

    def __repr__(self) -> str:
        return f"<Activity {self.name}>"
