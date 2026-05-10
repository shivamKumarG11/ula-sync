import os

from dotenv import load_dotenv
from flask import Flask, send_from_directory

from app.config import config
from app.extensions import bcrypt, cache, cors, db, jwt, limiter, migrate

load_dotenv()


def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    _init_extensions(app)
    _register_blueprints(app)
    _register_error_handlers(app)
    _ensure_upload_dir(app)
    _register_static_images(app)

    return app


def _init_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )
    cache.init_app(app)
    limiter.init_app(app)


def _register_blueprints(app: Flask) -> None:
    from app.routes import register_blueprints

    register_blueprints(app)


def _register_error_handlers(app: Flask) -> None:
    from app.utils.errors import register_error_handlers

    register_error_handlers(app)


def _ensure_upload_dir(app: Flask) -> None:
    upload_folder = app.config.get("UPLOAD_FOLDER", "./uploads")
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(os.path.join(upload_folder, "avatars"), exist_ok=True)
    os.makedirs(os.path.join(upload_folder, "trips"), exist_ok=True)


def _register_static_images(app: Flask) -> None:
    """Serve the data/ folder images at /images/<path> so the frontend can use them."""
    data_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data")
    )

    @app.route("/images/<path:filename>")
    def serve_data_image(filename: str):
        return send_from_directory(data_dir, filename)
