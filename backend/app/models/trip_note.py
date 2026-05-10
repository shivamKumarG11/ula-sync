import uuid

from sqlalchemy import Column, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db
from app.models.mixins import TimestampMixin


class TripNote(TimestampMixin, db.Model):
    __tablename__ = "trip_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False,
    )
    stop_id = Column(
        UUID(as_uuid=True),
        ForeignKey("stops.id", ondelete="SET NULL"),
        nullable=True,
    )
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)

    trip = db.relationship("Trip", back_populates="notes")
    stop = db.relationship("Stop", back_populates="trip_notes")

    __table_args__ = (
        Index("trip_notes_trip_id_idx", "trip_id"),
        Index("trip_notes_stop_id_idx", "stop_id"),
    )

    def __repr__(self) -> str:
        return f"<TripNote {self.title[:30]}>"
