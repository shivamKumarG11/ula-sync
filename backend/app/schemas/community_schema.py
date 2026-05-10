from marshmallow import Schema, fields, validate


class CommunityPostInputSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    content = fields.Str(required=True, validate=validate.Length(min=1, max=10000))
    trip_slug = fields.Str(allow_none=True, load_default=None)
    city_slug = fields.Str(allow_none=True, load_default=None)
    image_urls = fields.List(
        fields.Str(), validate=validate.Length(max=5), load_default=[]
    )


class CommunityPostUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=200))
    content = fields.Str(validate=validate.Length(min=1, max=10000))
    image_urls = fields.List(fields.Str(), validate=validate.Length(max=5))


class UserMinimalSchema(Schema):
    id = fields.UUID()
    username = fields.Str()
    full_name = fields.Str()
    profile_photo_url = fields.Str(allow_none=True)


class TripRefSchema(Schema):
    slug = fields.Str()
    name = fields.Str()


class CityRefSchema(Schema):
    slug = fields.Str()
    name = fields.Str()


class CommunityPostOutputSchema(Schema):
    id = fields.UUID()
    user = fields.Nested(UserMinimalSchema)
    trip = fields.Nested(TripRefSchema, allow_none=True)
    city = fields.Nested(CityRefSchema, allow_none=True)
    title = fields.Str()
    content = fields.Str()
    image_urls = fields.List(fields.Str())
    likes_count = fields.Int()
    comments_count = fields.Int()
    is_liked_by_me = fields.Bool(dump_default=False)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class CommentInputSchema(Schema):
    content = fields.Str(required=True, validate=validate.Length(min=1, max=2000))


class CommentOutputSchema(Schema):
    id = fields.UUID()
    post_id = fields.UUID()
    user = fields.Nested(UserMinimalSchema)
    content = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
