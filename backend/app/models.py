"""Database model for stored prediction history."""

from datetime import datetime, timezone

from app.extensions import db


class Customer(db.Model):
    """A customer identified by a simple, reusable dashboard-facing code."""

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(20), nullable=False, unique=True, index=True)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    predictions = db.relationship(
        "PredictionRecord", back_populates="customer", lazy="dynamic", cascade="all, delete-orphan"
    )


class PredictionRecord(db.Model):
    """One customer prediction and the raw values used to calculate it."""

    __tablename__ = "prediction_records"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False, index=True)
    customer = db.relationship("Customer", back_populates="predictions")
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
    selected_model = db.Column(db.String(64), nullable=False)
    model_predictions = db.Column(db.JSON, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
