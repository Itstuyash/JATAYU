import os
from flask import Flask
from dotenv import load_dotenv
from .models import db
from .routes.predict import predict_bp

def create_app():
    load_dotenv()
    app=Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///default.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    app.register_blueprint(predict_bp)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app