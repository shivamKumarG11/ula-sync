from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class StopInputSchema(Schema):
    city_id = fields.UUID(required=True)
    arrival_date = fields.Date(required=True)
    departure_date = fields.Date(required=True)
    order_index = fields.Int(load_default=None)
    notes = fields.Str(allow_none=True, load_default=None)

    @validates_schema
    def validate_dates(self, data, **kwargs):
        if "arrival_date" in data and "departure_date" in data:
            if data["departure_date"] < data["arrival_date"]:
                raise ValidationError("departure_date must be >= arrival_date")


class StopUpdateSchema(Schema):
    arrival_date = fields.Date()
    departure_date = fields.Date()
    notes = fields.Str(allow_none=True)


class CitySummarySchema(Schema):
    id = fields.UUID()
    slug = fields.Str()
    name = fields.Str()
    country = fields.Str()
    cover_photo_url = fields.Str(allow_none=True)


class StopOutputSchema(Schema):
    id = fields.UUID()
    city = fields.Nested(CitySummarySchema)
    order_index = fields.Int()
    arrival_date = fields.Date()
    departure_date = fields.Date()
    notes = fields.Str(allow_none=True)
    activity_count = fields.Int(dump_default=0)
    created_at = fields.DateTime()


class ReorderStopsSchema(Schema):
    stop_ids = fields.List(fields.UUID(), required=True)
