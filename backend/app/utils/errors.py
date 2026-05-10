from http import HTTPStatus

from flask import Flask, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException


class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}


def _error_response(message: str, status_code: int, details: dict | None = None):
    body = {"error": message}
    if details:
        body["details"] = details
    return jsonify(body), status_code


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(exc: AppError):
        return _error_response(exc.message, exc.status_code, exc.details)

    @app.errorhandler(ValidationError)
    def handle_validation_error(exc: ValidationError):
        return _error_response("Validation failed", HTTPStatus.UNPROCESSABLE_ENTITY, exc.messages)

    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        return _error_response(exc.description or exc.name, exc.code)

    @app.errorhandler(Exception)
    def handle_unexpected(exc: Exception):
        app.logger.exception("Unhandled exception: %s", exc)
        return _error_response("An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR)
