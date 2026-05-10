import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    Enum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    Time,
)
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db
from app.models.enums import ActivityCategoryEnum
from app.models.mixins import TimestampMixin


class StopActivity(TimestampMixin, db.Model):
    __tablename__ = "stop_activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    stop_id = Column(
        UUID(as_uuid=True),
        ForeignKey("stops.id", ondelete="CASCADE"),
        nullable=False,
    )
    activity_id = Column(
        UUID(as_uuid=True),
        ForeignKey("activities.id", ondelete="SET NULL"),
        nullable=True,
    )
    custom_name = Column(String(200), nullable=True)
    custom_cost_usd = Column(Numeric(8, 2), nullable=True)
    category = Column(
        Enum(ActivityCategoryEnum, name="activity_category_enum"),
        nullable=False,
        default=ActivityCategoryEnum.other,
    )
    scheduled_date = Column(Date, nullable=True)
    scheduled_time = Column(Time, nullable=True)
    duration_hours = Column(Numeric(4, 1), nullable=True)
    notes = Column(Text, nullable=True)

    stop = db.relationship("Stop", back_populates="activities")
    activity = db.relationship("Activity", back_populates="stop_activities")

    __table_args__ = (
        CheckConstraint(
            "activity_id IS NOT NULL OR custom_name IS NOT NULL",
            name="stop_activity_requires_name_or_id",
        ),
        Index("stop_activities_stop_id_idx", "stop_id"),
        Index("stop_activities_activity_id_idx", "activity_id"),
        Index("stop_activities_date_idx", "stop_id", "scheduled_date"),
    )

    def __repr__(self) -> str:
        return f"<StopActivity stop={self.stop_id} activity={self.activity_id or self.custom_name}>"
