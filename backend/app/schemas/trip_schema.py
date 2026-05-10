from marshmallow import Schema, fields, validate


class TripInputSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=200))
    description = fields.Str(validate=validate.Length(max=2000), allow_none=True, load_default=None)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    cover_photo_url = fields.Str(allow_none=True, load_default=None)


class TripUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=2, max=200))
    description = fields.Str(validate=validate.Length(max=2000), allow_none=True)
    start_date = fields.Date()
    end_date = fields.Date()
    cover_photo_url = fields.Str(allow_none=True)
    is_public = fields.Bool()


class TripOutputSchema(Schema):
    id = fields.UUID()
    slug = fields.Str()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    start_date = fields.Date()
    end_date = fields.Date()
    cover_photo_url = fields.Str(allow_none=True)
    is_public = fields.Bool()
    share_token = fields.Str(allow_none=True)
    checklist_share_token = fields.Str(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class TripListOutputSchema(Schema):
    id = fields.UUID()
    slug = fields.Str()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    start_date = fields.Date()
    end_date = fields.Date()
    cover_photo_url = fields.Str(allow_none=True)
    is_public = fields.Bool()
    stop_count = fields.Int(dump_default=0)
    created_at = fields.DateTime()
