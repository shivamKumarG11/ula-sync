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
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, UUID

from app.extensions import db
from app.models.enums import InvoiceCategoryEnum, InvoiceStatusEnum
from app.models.mixins import TimestampMixin


class Invoice(TimestampMixin, db.Model):
    __tablename__ = "invoices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(
        UUID(as_uuid=True),
        ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    invoice_number = Column(String(50), nullable=False, unique=True)
    status = Column(
        Enum(InvoiceStatusEnum, name="invoice_status_enum"),
        nullable=False,
        default=InvoiceStatusEnum.draft,
    )
    tax_percent = Column(Numeric(5, 2), nullable=False, default=5.00)
    discount_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    traveler_names = Column(JSONB, nullable=False, default=list)
    paid_at = Column(TIMESTAMP(timezone=True), nullable=True)

    trip = db.relationship("Trip", back_populates="invoice")
    items = db.relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan",
        order_by="InvoiceItem.order_index",
        lazy="select",
    )

    __table_args__ = (
        __import__("sqlalchemy", fromlist=["CheckConstraint"]).CheckConstraint(
            "tax_percent >= 0 AND tax_percent <= 100", name="invoice_tax_valid"
        ),
        __import__("sqlalchemy", fromlist=["CheckConstraint"]).CheckConstraint(
            "discount_amount >= 0", name="invoice_discount_positive"
        ),
        Index("invoices_trip_id_idx", "trip_id", unique=True),
        Index("invoices_number_idx", "invoice_number", unique=True),
    )

    def __repr__(self) -> str:
        return f"<Invoice {self.invoice_number}>"


class InvoiceItem(db.Model):
    __tablename__ = "invoice_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(
        UUID(as_uuid=True),
        ForeignKey("invoices.id", ondelete="CASCADE"),
        nullable=False,
    )
    category = Column(
        Enum(InvoiceCategoryEnum, name="invoice_category_enum"), nullable=False
    )
    description = Column(String(500), nullable=False)
    qty_details = Column(String(200), nullable=False)
    quantity = Column(Numeric(6, 2), nullable=False, default=1)
    unit_cost = Column(Numeric(10, 2), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    order_index = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    invoice = db.relationship("Invoice", back_populates="items")

    __table_args__ = (
        __import__("sqlalchemy", fromlist=["CheckConstraint"]).CheckConstraint(
            "unit_cost >= 0", name="invoice_item_unit_cost_positive"
        ),
        __import__("sqlalchemy", fromlist=["CheckConstraint"]).CheckConstraint(
            "amount >= 0", name="invoice_item_amount_positive"
        ),
        __import__("sqlalchemy", fromlist=["CheckConstraint"]).CheckConstraint(
            "quantity > 0", name="invoice_item_quantity_positive"
        ),
        Index("invoice_items_invoice_id_idx", "invoice_id"),
    )

    def __repr__(self) -> str:
        return f"<InvoiceItem {self.description[:30]}>"
