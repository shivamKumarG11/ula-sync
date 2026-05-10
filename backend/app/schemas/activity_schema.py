from marshmallow import Schema, fields, validate


class ActivityOutputSchema(Schema):
    id = fields.UUID()
    city_id = fields.UUID(allow_none=True)
    name = fields.Str()
    description = fields.Str(allow_none=True)
    category = fields.Str()
    cost_usd = fields.Decimal(as_string=True)
    duration_hours = fields.Decimal(as_string=True, allow_none=True)
    image_url = fields.Str(allow_none=True)
    map_link = fields.Str(allow_none=True)
    opening_time = fields.Time(allow_none=True)
    closing_time = fields.Time(allow_none=True)
    booking_required = fields.Bool()
    booking_link = fields.Str(allow_none=True)
    created_at = fields.DateTime()


class StopActivityInputSchema(Schema):
    activity_id = fields.UUID(allow_none=True, load_default=None)
    custom_name = fields.Str(validate=validate.Length(max=200), allow_none=True, load_default=None)
    custom_cost_usd = fields.Decimal(allow_none=True, load_default=None)
    category = fields.Str(load_default="other")
    scheduled_date = fields.Date(allow_none=True, load_default=None)
    scheduled_time = fields.Time(allow_none=True, load_default=None)
    duration_hours = fields.Decimal(allow_none=True, load_default=None)
    notes = fields.Str(allow_none=True, load_default=None)


class StopActivityUpdateSchema(Schema):
    custom_name = fields.Str(validate=validate.Length(max=200), allow_none=True)
    custom_cost_usd = fields.Decimal(allow_none=True)
    category = fields.Str()
    scheduled_date = fields.Date(allow_none=True)
    scheduled_time = fields.Time(allow_none=True)
    duration_hours = fields.Decimal(allow_none=True)
    notes = fields.Str(allow_none=True)


class ActivitySummarySchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    category = fields.Str()


class StopActivityOutputSchema(Schema):
    id = fields.UUID()
    activity = fields.Nested(ActivitySummarySchema, allow_none=True)
    custom_name = fields.Str(allow_none=True)
    effective_cost_usd = fields.Method("get_effective_cost")
    category = fields.Str()
    scheduled_date = fields.Date(allow_none=True)
    scheduled_time = fields.Time(allow_none=True)
    duration_hours = fields.Decimal(as_string=True, allow_none=True)
    notes = fields.Str(allow_none=True)
    created_at = fields.DateTime()

    def get_effective_cost(self, obj):
        if obj.custom_cost_usd is not None:
            return str(obj.custom_cost_usd)
        if obj.activity and obj.activity.cost_usd is not None:
            return str(obj.activity.cost_usd)
        return "0.00"
