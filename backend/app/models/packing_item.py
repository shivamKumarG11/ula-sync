import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db
from app.models.enums import PackingCategoryEnum
from app.models.mixins import TimestampMixin


class PackingItem(TimestampMixin, db.Model):
    __tablename__ = "packing_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(String(200), nullable=False)
    category = Column(
        Enum(PackingCategoryEnum, name="packing_category_enum"), nullable=False
    )
    is_packed = Column(Boolean, nullable=False, default=False)
    is_compulsory = Column(Boolean, nullable=False, default=False)

    trip = db.relationship("Trip", back_populates="packing_items")

    __table_args__ = (
        Index("packing_items_trip_id_idx", "trip_id"),
        Index("packing_items_trip_category_idx", "trip_id", "category"),
    )

    def __repr__(self) -> str:
        return f"<PackingItem {self.name}>"
