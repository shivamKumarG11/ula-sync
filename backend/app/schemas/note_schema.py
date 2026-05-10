from marshmallow import Schema, fields, validate


class NoteInputSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    content = fields.Str(required=True, validate=validate.Length(min=1, max=10000))
    stop_id = fields.UUID(allow_none=True, load_default=None)


class NoteUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=200))
    content = fields.Str(validate=validate.Length(min=1, max=10000))


class NoteOutputSchema(Schema):
    id = fields.UUID()
    trip_id = fields.UUID()
    stop_id = fields.UUID(allow_none=True)
    title = fields.Str()
    content = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
