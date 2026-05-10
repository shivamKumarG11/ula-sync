from datetime import datetime, timezone

from app.extensions import db
from app.models import Invoice, InvoiceItem, Trip
from app.models.enums import InvoiceStatusEnum
from app.utils.errors import AppError


def _invoice_number(invoice_id) -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    short = str(invoice_id).replace("-", "")[:6].upper()
    return f"INV-{today}-{short}"


def _compute_totals(invoice: Invoice) -> dict:
    subtotal = sum(item.amount for item in invoice.items)
    tax_amount = subtotal * (invoice.tax_percent / 100)
    grand_total = subtotal + tax_amount - invoice.discount_amount
    return {
        "subtotal": float(subtotal),
        "tax_amount": float(tax_amount),
        "grand_total": float(grand_total),
    }


def get_invoice(trip: Trip) -> Invoice:
    inv = Invoice.query.filter_by(trip_id=trip.id).first()
    if not inv:
        raise AppError("Invoice not found", 404)
    return inv


def create_invoice(trip: Trip, data: dict) -> Invoice:
    if Invoice.query.filter_by(trip_id=trip.id).first():
        raise AppError("Invoice already exists for this trip", 409)

    inv = Invoice(
        trip_id=trip.id,
        tax_percent=data.get("tax_percent", 5.00),
        discount_amount=data.get("discount_amount", 0.00),
        traveler_names=data.get("traveler_names", []),
    )
    db.session.add(inv)
    db.session.flush()
    inv.invoice_number = _invoice_number(inv.id)
    db.session.commit()
    return inv


def update_invoice(inv: Invoice, data: dict) -> Invoice:
    for key in ("tax_percent", "discount_amount", "traveler_names"):
        if key in data:
            setattr(inv, key, data[key])

    if "status" in data:
        new_status = data["status"]
        inv.status = new_status
        if new_status == InvoiceStatusEnum.paid.value and not inv.paid_at:
            inv.paid_at = datetime.now(timezone.utc)

    db.session.commit()
    return inv


def add_item(inv: Invoice, data: dict) -> InvoiceItem:
    max_order = (
        db.session.query(db.func.max(InvoiceItem.order_index))
        .filter_by(invoice_id=inv.id)
        .scalar()
    )
    item = InvoiceItem(
        invoice_id=inv.id,
        category=data["category"],
        description=data["description"],
        qty_details=data["qty_details"],
        quantity=data.get("quantity", 1),
        unit_cost=data["unit_cost"],
        amount=data["amount"],
        order_index=(max_order or -1) + 1,
    )
    db.session.add(item)
    db.session.commit()
    return item


def get_item(item_id: str, inv: Invoice) -> InvoiceItem:
    item = InvoiceItem.query.filter_by(id=item_id, invoice_id=inv.id).first()
    if not item:
        raise AppError("Invoice item not found", 404)
    return item


def update_item(item: InvoiceItem, data: dict) -> InvoiceItem:
    for key in ("category", "description", "qty_details", "quantity", "unit_cost", "amount"):
        if key in data:
            setattr(item, key, data[key])
    db.session.commit()
    return item


def delete_item(item: InvoiceItem) -> None:
    db.session.delete(item)
    db.session.commit()


def build_invoice_pdf_data(inv: Invoice, trip: Trip) -> dict:
    totals = _compute_totals(inv)
    stop_names = [s.city.name for s in trip.stops.all()]
    return {
        "invoice_number": inv.invoice_number,
        "status": inv.status.value if hasattr(inv.status, "value") else inv.status,
        "tax_percent": float(inv.tax_percent),
        "discount_amount": float(inv.discount_amount),
        "traveler_names": inv.traveler_names or [],
        "items": [
            {
                "description": i.description,
                "qty_details": i.qty_details,
                "unit_cost": float(i.unit_cost),
                "amount": float(i.amount),
            }
            for i in inv.items
        ],
        "trip": {
            "name": trip.name,
            "start_date": str(trip.start_date),
            "end_date": str(trip.end_date),
        },
        **totals,
    }
