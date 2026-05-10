from marshmallow import Schema, fields, validate


class InvoiceCreateSchema(Schema):
    tax_percent = fields.Decimal(load_default=5.00)
    discount_amount = fields.Decimal(load_default=0.00)
    traveler_names = fields.List(fields.Str(), load_default=[])


class InvoiceUpdateSchema(Schema):
    tax_percent = fields.Decimal()
    discount_amount = fields.Decimal()
    traveler_names = fields.List(fields.Str())
    status = fields.Str(
        validate=validate.OneOf(["draft", "pending", "paid"])
    )


class InvoiceItemInputSchema(Schema):
    category = fields.Str(required=True)
    description = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    qty_details = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    quantity = fields.Decimal(load_default=1)
    unit_cost = fields.Decimal(required=True)
    amount = fields.Decimal(required=True)


class InvoiceItemUpdateSchema(Schema):
    category = fields.Str()
    description = fields.Str(validate=validate.Length(min=1, max=500))
    qty_details = fields.Str(validate=validate.Length(min=1, max=200))
    quantity = fields.Decimal()
    unit_cost = fields.Decimal()
    amount = fields.Decimal()


class InvoiceItemOutputSchema(Schema):
    id = fields.UUID()
    category = fields.Str()
    description = fields.Str()
    qty_details = fields.Str()
    quantity = fields.Decimal(as_string=True)
    unit_cost = fields.Decimal(as_string=True)
    amount = fields.Decimal(as_string=True)
    order_index = fields.Int()
    created_at = fields.DateTime()


class TripRefSchema(Schema):
    name = fields.Str()
    start_date = fields.Date()
    end_date = fields.Date()
    stop_names = fields.List(fields.Str(), dump_default=[])


class InvoiceOutputSchema(Schema):
    id = fields.UUID()
    invoice_number = fields.Str()
    status = fields.Str()
    tax_percent = fields.Decimal(as_string=True)
    discount_amount = fields.Decimal(as_string=True)
    traveler_names = fields.List(fields.Str())
    paid_at = fields.DateTime(allow_none=True)
    items = fields.List(fields.Nested(InvoiceItemOutputSchema))
    subtotal = fields.Decimal(as_string=True, dump_default="0.00")
    tax_amount = fields.Decimal(as_string=True, dump_default="0.00")
    grand_total = fields.Decimal(as_string=True, dump_default="0.00")
    trip = fields.Nested(TripRefSchema, dump_default=None)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
