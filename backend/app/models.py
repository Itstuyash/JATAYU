"""Database model for stored prediction history."""

from datetime import datetime, timezone

from app.extensions import db


class PredictionRecord(db.Model):
    """One customer prediction and the raw values used to calculate it."""

    __tablename__ = "prediction_records"

    id = db.Column(db.Integer, primary_key=True)
    LIMIT_BAL = db.Column(db.Float, nullable=False)
    AGE = db.Column(db.Float, nullable=False)
    PAY_0 = db.Column(db.Float, nullable=False)

    BILL_AMT1 = db.Column(db.Float, nullable=False)
    BILL_AMT2 = db.Column(db.Float, nullable=False)
    BILL_AMT3 = db.Column(db.Float, nullable=False)
    BILL_AMT4 = db.Column(db.Float, nullable=False)
    BILL_AMT5 = db.Column(db.Float, nullable=False)
    BILL_AMT6 = db.Column(db.Float, nullable=False)

    PAY_AMT1 = db.Column(db.Float, nullable=False)
    PAY_AMT2 = db.Column(db.Float, nullable=False)
    PAY_AMT3 = db.Column(db.Float, nullable=False)
    PAY_AMT4 = db.Column(db.Float, nullable=False)
    PAY_AMT5 = db.Column(db.Float, nullable=False)
    PAY_AMT6 = db.Column(db.Float, nullable=False)

    Total_bill = db.Column(db.Float, nullable=False)
    Total_pay = db.Column(db.Float, nullable=False)
    Outstanding = db.Column(db.Float, nullable=False)
    prediction = db.Column(db.Integer, nullable=False)
    prediction_label = db.Column(db.String(32), nullable=False)
    default_probability = db.Column(db.Float, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
