from marshmallow import Schema, fields, validate


class CostBreakdownOutputSchema(Schema):
    expense_type = fields.Str()
    cost_usd = fields.Decimal(as_string=True)
    cost_local = fields.Decimal(as_string=True)
    local_currency = fields.Str()
    description = fields.Str(allow_none=True)


class CityOutputSchema(Schema):
    id = fields.UUID()
    slug = fields.Str()
    name = fields.Str()
    country = fields.Str()
    country_code = fields.Str(allow_none=True)
    region = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    cover_photo_url = fields.Str(allow_none=True)
    map_link = fields.Str(allow_none=True)
    best_time_months = fields.Str(allow_none=True)
    cost_index_usd = fields.Decimal(as_string=True)
    popularity_score = fields.Int()
    latitude = fields.Decimal(as_string=True, allow_none=True)
    longitude = fields.Decimal(as_string=True, allow_none=True)
    timezone = fields.Str(allow_none=True)
    iata_code = fields.Str(allow_none=True)
    cost_breakdown = fields.List(fields.Nested(CostBreakdownOutputSchema), dump_default=[])
    activities = fields.List(fields.Nested("ActivityOutputSchema"), dump_default=[])
    created_at = fields.DateTime()


class CityListOutputSchema(Schema):
    id = fields.UUID()
    slug = fields.Str()
    name = fields.Str()
    country = fields.Str()
    country_code = fields.Str(allow_none=True)
    cover_photo_url = fields.Str(allow_none=True)
    cost_index_usd = fields.Decimal(as_string=True)
    popularity_score = fields.Int()
    iata_code = fields.Str(allow_none=True)
    latitude = fields.Decimal(as_string=True, allow_none=True)
    longitude = fields.Decimal(as_string=True, allow_none=True)
