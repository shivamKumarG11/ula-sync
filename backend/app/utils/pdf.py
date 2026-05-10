import io
from datetime import date

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def generate_invoice_pdf(invoice_data: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    brand_color = colors.HexColor("#1d4ed8")

    title_style = ParagraphStyle(
        "TraveloopTitle",
        parent=styles["Heading1"],
        textColor=brand_color,
        fontSize=22,
        spaceAfter=4,
    )
    sub_style = ParagraphStyle(
        "Sub", parent=styles["Normal"], fontSize=9, textColor=colors.gray
    )
    normal = styles["Normal"]

    story = []

    story.append(Paragraph("Traveloop", title_style))
    story.append(Paragraph("Travel Expense Invoice", sub_style))
    story.append(Spacer(1, 6 * mm))

    trip = invoice_data.get("trip", {})
    meta = [
        ["Invoice #", invoice_data.get("invoice_number", "")],
        ["Trip", trip.get("name", "")],
        ["Dates", f"{trip.get('start_date', '')} → {trip.get('end_date', '')}"],
        ["Status", invoice_data.get("status", "draft").upper()],
        ["Travelers", ", ".join(invoice_data.get("traveler_names", []))],
    ]
    meta_table = Table(meta, colWidths=[40 * mm, 130 * mm])
    meta_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(meta_table)
    story.append(Spacer(1, 8 * mm))

    headers = ["#", "Description", "Qty", "Unit Cost", "Amount"]
    rows = [headers]
    for i, item in enumerate(invoice_data.get("items", []), 1):
        rows.append(
            [
                str(i),
                item.get("description", ""),
                item.get("qty_details", ""),
                f"${item.get('unit_cost', 0):,.2f}",
                f"${item.get('amount', 0):,.2f}",
            ]
        )

    col_widths = [10 * mm, 80 * mm, 30 * mm, 25 * mm, 25 * mm]
    items_table = Table(rows, colWidths=col_widths, repeatRows=1)
    items_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), brand_color),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (3, 0), (-1, -1), "RIGHT"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(items_table)
    story.append(Spacer(1, 6 * mm))

    subtotal = invoice_data.get("subtotal", 0)
    tax_amount = invoice_data.get("tax_amount", 0)
    discount = invoice_data.get("discount_amount", 0)
    grand_total = invoice_data.get("grand_total", 0)
    tax_pct = invoice_data.get("tax_percent", 0)

    totals = [
        ["Subtotal", f"${subtotal:,.2f}"],
        [f"Tax ({tax_pct}%)", f"${tax_amount:,.2f}"],
        [f"Discount", f"-${discount:,.2f}"],
        ["Grand Total", f"${grand_total:,.2f}"],
    ]
    totals_table = Table(totals, colWidths=[130 * mm, 40 * mm])
    totals_table.setStyle(
        TableStyle(
            [
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, -1), (-1, -1), 11),
                ("LINEABOVE", (0, -1), (-1, -1), 0.5, colors.black),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(totals_table)

    doc.build(story)
    return buffer.getvalue()
