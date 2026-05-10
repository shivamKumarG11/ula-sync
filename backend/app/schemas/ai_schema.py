from marshmallow import Schema, fields, validate


class GenerateItineraryInputSchema(Schema):
    trip_slug = fields.Str(required=True)
    preferences = fields.Dict(load_default={})


class SuggestActivitiesInputSchema(Schema):
    city_slug = fields.Str(required=True)
    user_interests = fields.List(fields.Str(), load_default=[])
    budget_usd_per_day = fields.Float(load_default=50)
    days_available = fields.Int(load_default=3)
    existing_activity_ids = fields.List(fields.UUID(), load_default=[])


class RecommendTransportInputSchema(Schema):
    origin_city_slug = fields.Str(required=True)
    destination_city_slug = fields.Str(required=True)
    travel_date = fields.Date(required=True)
    priority = fields.Str(
        validate=validate.OneOf(["speed", "cost", "comfort", "experience"]),
        load_default="cost",
    )
    group_size = fields.Int(load_default=1)
    budget_usd = fields.Float(load_default=100)


class ReviewTripInputSchema(Schema):
    trip_slug = fields.Str(required=True)


class PackingAdviceInputSchema(Schema):
    trip_slug = fields.Str(required=True)
    existing_item_names = fields.List(fields.Str(), load_default=[])


class ChatMessageSchema(Schema):
    role = fields.Str(validate=validate.OneOf(["user", "assistant"]), required=True)
    content = fields.Str(required=True)


class ChatInputSchema(Schema):
    messages = fields.List(fields.Nested(ChatMessageSchema), required=True)
    context = fields.Dict(load_default={})
