from flask import Blueprint, g, request, send_file
import io

from app.middleware.auth_middleware import require_auth
from app.schemas.invoice_schema import (
    InvoiceInputSchema,
    InvoiceItemInputSchema,
    InvoiceItemOutputSchema,
    InvoiceItemUpdateSchema,
    InvoiceOutputSchema,
    InvoiceUpdateSchema,
)
from app.services import invoice_service, trip_service
from app.utils.helpers import make_response_envelope
from app.utils.pdf import generate_invoice_pdf
from webargs.flaskparser import use_args

invoice_bp = Blueprint("invoice", __name__, url_prefix="/api/v1/trips/<trip_slug>/invoice")


def _trip_and_invoice(trip_slug, *, require_invoice=True):
    trip = trip_service.get_trip(trip_slug, g.current_user)
    if require_invoice:
        inv = invoice_service.get_invoice(trip)
        return trip, inv
    return trip


@invoice_bp.get("/")
@require_auth
def get_invoice(trip_slug):
    trip, inv = _trip_and_invoice(trip_slug)
    return make_response_envelope(InvoiceOutputSchema().dump(inv)), 200


@invoice_bp.post("/")
@require_auth
@use_args(InvoiceInputSchema(), location="json")
def create_invoice(args, trip_slug):
    trip = _trip_and_invoice(trip_slug, require_invoice=False)
    inv = invoice_service.create_invoice(trip, args)
    return make_response_envelope(InvoiceOutputSchema().dump(inv)), 201


@invoice_bp.put("/")
@require_auth
@use_args(InvoiceUpdateSchema(), location="json")
def update_invoice(args, trip_slug):
    trip, inv = _trip_and_invoice(trip_slug)
    inv = invoice_service.update_invoice(inv, args)
    return make_response_envelope(InvoiceOutputSchema().dump(inv)), 200


@invoice_bp.post("/items")
@require_auth
@use_args(InvoiceItemInputSchema(), location="json")
def add_item(args, trip_slug):
    trip, inv = _trip_and_invoice(trip_slug)
    item = invoice_service.add_item(inv, args)
    return make_response_envelope(InvoiceItemOutputSchema().dump(item)), 201


@invoice_bp.put("/items/<item_id>")
@require_auth
@use_args(InvoiceItemUpdateSchema(), location="json")
def update_item(args, trip_slug, item_id):
    trip, inv = _trip_and_invoice(trip_slug)
    item = invoice_service.get_item(item_id, inv)
    item = invoice_service.update_item(item, args)
    return make_response_envelope(InvoiceItemOutputSchema().dump(item)), 200


@invoice_bp.delete("/items/<item_id>")
@require_auth
def delete_item(trip_slug, item_id):
    trip, inv = _trip_and_invoice(trip_slug)
    item = invoice_service.get_item(item_id, inv)
    invoice_service.delete_item(item)
    return "", 204


@invoice_bp.get("/export")
@require_auth
def export_pdf(trip_slug):
    trip, inv = _trip_and_invoice(trip_slug)
    pdf_data = invoice_service.build_invoice_pdf_data(inv, trip)
    pdf_bytes = generate_invoice_pdf(pdf_data)
    filename = f"{inv.invoice_number}.pdf"
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )
