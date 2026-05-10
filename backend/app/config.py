import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False  # set True in production (HTTPS only)
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 900)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        seconds=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES", 604800))
    )

    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")

    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "./uploads")
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))

    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300

    RATELIMIT_STORAGE_URL = "memory://"

    # External APIs
    AMADEUS_API_KEY = os.environ.get("AMADEUS_API_KEY", "")
    AMADEUS_API_SECRET = os.environ.get("AMADEUS_API_SECRET", "")
    AMADEUS_BASE_URL = os.environ.get("AMADEUS_BASE_URL", "https://test.api.amadeus.com")
    OPENTRIPMAP_API_KEY = os.environ.get("OPENTRIPMAP_API_KEY", "")
    UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    TICKETMASTER_API_KEY = os.environ.get("TICKETMASTER_API_KEY", "")
    YELP_API_KEY = os.environ.get("YELP_API_KEY", "")
    AVIATIONSTACK_KEY = os.environ.get("AVIATIONSTACK_KEY", "")

    # AI
    TOKEN_ROUTER_API_KEY = os.environ.get("TOKEN_ROUTER_API_KEY", "")
    TOKEN_ROUTER_BASE_URL = os.environ.get(
        "TOKEN_ROUTER_BASE_URL", "https://api.tokenrouter.com/v1"
    )


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://traveloop:traveloop@localhost:5432/traveloop"
    )
    SQLALCHEMY_ECHO = False  # set True to log SQL in dev if needed


class ProductionConfig(Config):
    DEBUG = False
    JWT_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL", "postgresql://traveloop:traveloop@localhost:5432/traveloop_test"
    )
    JWT_COOKIE_CSRF_PROTECT = False
    WTF_CSRF_ENABLED = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
