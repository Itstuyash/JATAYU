"""Flask application factory for the Credit Card Default Prediction API."""

from flask import Flask

from config import Config
from app.extensions import cors, db
from app.routes.health import health_bp
from app.routes.predict import predict_bp
from app.routes.dashboard import dashboard_bp


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    app.register_blueprint(health_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(dashboard_bp)

    with app.app_context():
        db.create_all()

    return app
