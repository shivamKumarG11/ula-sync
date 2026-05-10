from flask import Blueprint, g, make_response, request

from app.middleware.auth_middleware import require_auth
from app.schemas.user_schema import LoginInputSchema, RegisterInputSchema, UserOutputSchema
from app.services import auth_service
from app.utils.helpers import make_response_envelope
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    verify_jwt_in_request,
)
from webargs.flaskparser import use_args

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


def _set_tokens(response, user_id: str):
    access_token = create_access_token(identity=str(user_id))
    refresh_token = create_refresh_token(identity=str(user_id))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)


@auth_bp.post("/register")
@use_args(RegisterInputSchema(), location="json")
def register(args):
    user = auth_service.register_user(args)
    schema = UserOutputSchema()
    resp = make_response(make_response_envelope({"user": schema.dump(user)}, "Account created successfully"), 201)
    _set_tokens(resp, user.id)
    return resp


@auth_bp.post("/login")
@use_args(LoginInputSchema(), location="json")
def login(args):
    user = auth_service.login_user(args["email"], args["password"])
    schema = UserOutputSchema()
    resp = make_response(make_response_envelope({"user": schema.dump(user)}), 200)
    _set_tokens(resp, user.id)
    return resp


@auth_bp.post("/refresh")
def refresh():
    verify_jwt_in_request(locations=["cookies"], refresh=True)
    user_id = get_jwt_identity()
    resp = make_response(make_response_envelope(None, "Token refreshed"), 200)
    new_token = create_access_token(identity=str(user_id))
    set_access_cookies(resp, new_token)
    return resp


@auth_bp.post("/logout")
def logout():
    resp = make_response(make_response_envelope(None, "Logged out"), 200)
    unset_jwt_cookies(resp)
    return resp


@auth_bp.get("/me")
@require_auth
def me():
    schema = UserOutputSchema()
    return make_response_envelope(schema.dump(g.current_user)), 200
