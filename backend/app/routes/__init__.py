from .auth import auth_bp
from .users import users_bp
from .trips import trips_bp
from .stops import stops_bp
from .stop_activities import stop_activities_bp
from .cities import cities_bp
from .activities import activities_bp
from .budget import budget_bp
from .notes import notes_bp
from .packing import packing_bp
from .invoice import invoice_bp
from .community import community_bp
from .ai import ai_bp
from .admin import admin_bp
from .saved_cities import saved_cities_bp
from .external import external_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(stops_bp)
    app.register_blueprint(stop_activities_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(activities_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(packing_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(saved_cities_bp)
    app.register_blueprint(external_bp)
