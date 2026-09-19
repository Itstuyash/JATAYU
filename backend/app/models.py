from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LivePrediction(db.Model):
    __tablename__ = 'live_prediction'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Float, nullable=False)
    income = db.Column(db.Float, nullable=False)
    loan=db.Column(db.Float, nullable=False)
    loan_to_income_ratio=db.Column(db.Float, nullable=False)
    prediction = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())