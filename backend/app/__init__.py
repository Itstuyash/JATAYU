import os
from flask import Flask
from dotenv import load_dotenv
from .routes.predict import predict_bp

def create_app():
    load_dotenv()
    app=Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    app.register_blueprint(predict_bp)
    
    return app