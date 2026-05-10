from marshmallow import Schema, fields, validate


class PackingItemInputSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    category = fields.Str(required=True)
    is_compulsory = fields.Bool(load_default=False)


class PackingItemUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=200))
    category = fields.Str()
    is_packed = fields.Bool()
    is_compulsory = fields.Bool()


class PackingItemOutputSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    category = fields.Str()
    is_packed = fields.Bool()
    is_compulsory = fields.Bool()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class PackingBatchInputSchema(Schema):
    items = fields.List(fields.Nested(PackingItemInputSchema), required=True)
