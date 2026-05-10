from marshmallow import Schema, ValidationError, fields, validate, validates, validates_schema
from marshmallow_enum import EnumField

from app.models.enums import TravelStyleEnum


class RegisterInputSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8),
        load_only=True,
    )
    full_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))

    @validates("password")
    def validate_password(self, value):
        if not any(c.isupper() for c in value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(c.isdigit() for c in value):
            raise ValidationError("Password must contain at least one number.")


class LoginInputSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserOutputSchema(Schema):
    id = fields.UUID(dump_default=None)
    email = fields.Email()
    username = fields.Str()
    full_name = fields.Str()
    phone_number = fields.Str(allow_none=True)
    home_city = fields.Str(allow_none=True)
    home_country = fields.Str(allow_none=True)
    bio = fields.Str(allow_none=True)
    job_title = fields.Str(allow_none=True)
    company = fields.Str(allow_none=True)
    interests = fields.List(fields.Str())
    travel_style = fields.Str(allow_none=True)
    date_of_birth = fields.Date(allow_none=True)
    profile_photo_url = fields.Str(allow_none=True)
    language_preference = fields.Str()
    preferred_currency = fields.Str()
    is_admin = fields.Bool()
    onboarding_completed = fields.Bool()
    created_at = fields.DateTime()


class UserMinimalOutputSchema(Schema):
    id = fields.UUID()
    username = fields.Str()
    full_name = fields.Str()
    profile_photo_url = fields.Str(allow_none=True)


class UpdateProfileInputSchema(Schema):
    full_name = fields.Str(validate=validate.Length(min=2, max=100))
    bio = fields.Str(validate=validate.Length(max=500), allow_none=True)
    job_title = fields.Str(validate=validate.Length(max=100), allow_none=True)
    company = fields.Str(validate=validate.Length(max=100), allow_none=True)
    home_city = fields.Str(validate=validate.Length(max=100), allow_none=True)
    home_country = fields.Str(validate=validate.Length(max=100), allow_none=True)
    date_of_birth = fields.Date(allow_none=True)
    interests = fields.List(fields.Str(validate=validate.Length(max=50)), validate=validate.Length(max=10))
    travel_style = fields.Str(
        validate=validate.OneOf([e.value for e in TravelStyleEnum]), allow_none=True
    )
    language_preference = fields.Str(validate=validate.Length(min=2, max=10))
    preferred_currency = fields.Str(validate=validate.Length(equal=3))
    profile_photo_url = fields.Str(allow_none=True)
    onboarding_completed = fields.Bool()
    phone_number = fields.Str(validate=validate.Length(max=20), allow_none=True)
