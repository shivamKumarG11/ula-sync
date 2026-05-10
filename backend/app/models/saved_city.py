import uuid

from sqlalchemy import Column, ForeignKey, Index, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from app.extensions import db


class SavedCity(db.Model):
    __tablename__ = "saved_cities"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    city_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False,
    )
    saved_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ),
    )

    user = db.relationship("User", back_populates="saved_cities")
    city = db.relationship("City", back_populates="saved_by")

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "city_id", name="pk_saved_cities"),
        Index("saved_cities_user_id_idx", "user_id"),
    )

    def __repr__(self) -> str:
        return f"<SavedCity user={self.user_id} city={self.city_id}>"
