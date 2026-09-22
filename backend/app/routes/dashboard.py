"""Dashboard, recent-prediction, and customer-history endpoints."""

from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from sqlalchemy import func

from app.models import Customer, PredictionRecord


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api")


def serialize_prediction(record):
    """Return one compact prediction record for the dashboard."""
    return {
        "prediction_id": record.id,
        "customer_code": record.customer.customer_code,
        "prediction": record.prediction,
        "prediction_label": record.prediction_label,
        "BILL_AMT1": record.BILL_AMT1,
        "PAY_AMT1": record.PAY_AMT1,
        "default_probability": record.default_probability,
        "selected_model": record.selected_model,
        "created_at": record.created_at.isoformat(),
    }


@dashboard_bp.get("/predictions/recent")
def recent_predictions():
    """Return the five most recently stored predictions."""
    limit = min(max(request.args.get("limit", 5, type=int), 1), 20)
    records = PredictionRecord.query.order_by(PredictionRecord.created_at.desc()).limit(limit).all()
    return jsonify({"success": True, "predictions": [serialize_prediction(record) for record in records]})


@dashboard_bp.get("/customers/<customer_code>")
def customer_history(customer_code):
    """Return prediction history for one generated customer code."""
    customer = Customer.query.filter_by(customer_code=customer_code.upper()).first_or_404()
    records = customer.predictions.order_by(PredictionRecord.created_at.desc()).all()
    return jsonify(
        {
            "success": True,
            "customer": {
                "customer_code": customer.customer_code,
                "created_at": customer.created_at.isoformat(),
                "predictions": [serialize_prediction(record) for record in records],
            },
        }
    )


@dashboard_bp.get("/dashboard")
def dashboard_summary():
    """Return shareable dashboard statistics and recent predictions."""
    total_predictions = PredictionRecord.query.count()
    total_customers = Customer.query.count()
    default_predictions = PredictionRecord.query.filter_by(prediction=1).count()
    today = datetime.now(timezone.utc).date()
    predictions_today = PredictionRecord.query.filter(
        func.date(PredictionRecord.created_at) == today
    ).count()
    recent = PredictionRecord.query.order_by(PredictionRecord.created_at.desc()).limit(5).all()
    latest_prediction = recent[0] if recent else None
    return jsonify(
        {
            "success": True,
            "stats": {
                "total_customers": total_customers,
                "total_predictions": total_predictions,
                "predictions_today": predictions_today,
                "default_predictions": default_predictions,
                "default_rate": (default_predictions / total_predictions) if total_predictions else 0,
                "best_model": latest_prediction.selected_model if latest_prediction else None,
            },
            "recent_predictions": [serialize_prediction(record) for record in recent],
        }
    )
