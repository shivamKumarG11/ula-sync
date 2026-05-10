import uuid

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy import Uuid as UUID

from app.extensions import db
from app.models.mixins import TimestampMixin


class Stop(TimestampMixin, db.Model):
    __tablename__ = "stops"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False,
    )
    city_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cities.id", ondelete="RESTRICT"),
        nullable=False,
    )
    order_index = Column(Integer, nullable=False)
    arrival_date = Column(Date, nullable=False)
    departure_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)

    trip = db.relationship("Trip", back_populates="stops")
    city = db.relationship("City", back_populates="stops")
    activities = db.relationship(
        "StopActivity",
        back_populates="stop",
        cascade="all, delete-orphan",
        order_by="StopActivity.scheduled_date, StopActivity.scheduled_time",
        lazy="dynamic",
    )
    trip_notes = db.relationship("TripNote", back_populates="stop", lazy="dynamic")

    __table_args__ = (
        CheckConstraint("departure_date >= arrival_date", name="stop_departure_after_arrival"),
        Index("stops_trip_id_idx", "trip_id"),
        Index("stops_trip_order_idx", "trip_id", "order_index"),
    )

    def __repr__(self) -> str:
        return f"<Stop trip={self.trip_id} city={self.city_id} order={self.order_index}>"
