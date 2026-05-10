import os

from flask import Blueprint, g, request

from app.middleware.auth_middleware import require_auth
from app.schemas.user_schema import UpdateProfileInputSchema, UserOutputSchema
from app.services import auth_service
from app.utils.errors import AppError
from app.utils.helpers import make_response_envelope
from webargs.flaskparser import use_args

users_bp = Blueprint("users", __name__, url_prefix="/api/v1/users")

_ALLOWED_IMAGE_MIMES = {"image/jpeg", "image/png", "image/webp"}
_MAX_AVATAR_BYTES = 5 * 1024 * 1024  # 5 MB


@users_bp.put("/me")
@require_auth
@use_args(UpdateProfileInputSchema(), location="json")
def update_profile(args):
    user = auth_service.update_user_profile(g.current_user, args)
    return make_response_envelope(UserOutputSchema().dump(user)), 200


@users_bp.delete("/me")
@require_auth
def delete_account():
    auth_service.delete_user(g.current_user)
    return "", 204


@users_bp.post("/me/avatar")
@require_auth
def upload_avatar():
    if "photo" not in request.files:
        raise AppError("No file provided", 400)

    photo = request.files["photo"]
    if photo.mimetype not in _ALLOWED_IMAGE_MIMES:
        raise AppError("Unsupported media type. Use JPEG, PNG or WEBP.", 415)

    photo.seek(0, 2)
    size = photo.tell()
    photo.seek(0)
    if size > _MAX_AVATAR_BYTES:
        raise AppError("File too large. Maximum 5 MB.", 413)

    upload_folder = os.path.join(
        os.environ.get("UPLOAD_FOLDER", "uploads"), "avatars"
    )
    os.makedirs(upload_folder, exist_ok=True)

    ext = photo.mimetype.split("/")[-1].replace("jpeg", "jpg")
    filename = f"{g.current_user.id}.{ext}"
    filepath = os.path.join(upload_folder, filename)
    photo.save(filepath)

    url = f"/uploads/avatars/{filename}"
    g.current_user.profile_photo_url = url

    from app.extensions import db
    db.session.commit()

    return make_response_envelope({"profile_photo_url": url}), 200
