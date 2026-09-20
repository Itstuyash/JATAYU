"""Prediction endpoint backed by the saved ML pipeline."""

from functools import lru_cache
import json
from pathlib import Path

import joblib
import pandas as pd
import shap
from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.extensions import db
from app.models import PredictionRecord
from app.schemas import PredictionRequest
from ml.feature_engineering import MODEL_FEATURES
from ml.inference import transform_for_classifier


predict_bp = Blueprint("predict", __name__, url_prefix="/api")
PIPELINE_PATH = Path(__file__).resolve().parents[2] / "ml" / "credit_card_default_pipeline.pkl"
ML_DIRECTORY = PIPELINE_PATH.parent
MODEL_PATHS = {
    "Random Forest": PIPELINE_PATH,
    "Logistic Regression": ML_DIRECTORY / "logistic_regression_pipeline.pkl",
    "XGBoost": ML_DIRECTORY / "xgboost_pipeline.pkl",
}
METRICS_PATH = ML_DIRECTORY / "model_metrics.json"
SHAP_BACKGROUNDS_PATH = ML_DIRECTORY / "shap_backgrounds.pkl"


@lru_cache(maxsize=1)
def get_model_assets():
    """Load saved pipelines, model metrics, and SHAP backgrounds once."""
    required_files = [*MODEL_PATHS.values(), METRICS_PATH, SHAP_BACKGROUNDS_PATH]
    missing_files = [file.name for file in required_files if not file.exists()]
    if missing_files:
        raise FileNotFoundError("Missing trained model files: " + ", ".join(missing_files))

    with METRICS_PATH.open(encoding="utf-8") as metrics_file:
        metrics = json.load(metrics_file)
    return {
        "pipelines": {name: joblib.load(path) for name, path in MODEL_PATHS.items()},
        "metrics": metrics,
        "backgrounds": joblib.load(SHAP_BACKGROUNDS_PATH),
    }


def get_shap_explanation(model_name, pipeline, raw_frame, background):
    """Return per-feature SHAP contributions toward default probability."""
    classifier_input = transform_for_classifier(pipeline, raw_frame)
    classifier = pipeline.named_steps["classifier"]

    if model_name == "Logistic Regression":
        explainer = shap.LinearExplainer(classifier, background)
    elif model_name == "XGBoost":
        # Current SHAP/XGBoost versions require this supported mode for the
        # XGBoost model's categorical-split capability checks.
        explainer = shap.TreeExplainer(
            classifier, feature_perturbation="tree_path_dependent"
        )
    else:
        explainer = shap.TreeExplainer(classifier, data=background)

    values = explainer.shap_values(classifier_input)
    if isinstance(values, list):
        contributions = values[1][0]
    elif getattr(values, "ndim", 0) == 3:
        contributions = values[0, :, 1]
    else:
        contributions = values[0]

    engineered = pipeline.named_steps["feature_engineering"].transform(raw_frame).iloc[0]
    explanation = [
        {
            "feature": feature,
            "value": float(engineered[feature]),
            "contribution": float(contribution),
        }
        for feature, contribution in zip(MODEL_FEATURES, contributions)
    ]
    return sorted(explanation, key=lambda item: abs(item["contribution"]), reverse=True)


@predict_bp.post("/predict")
def predict():
    """Validate raw customer input, predict risk, and store the outcome."""
    try:
        payload = PredictionRequest.model_validate(request.get_json(silent=True))
    except ValidationError as error:
        return jsonify({"success": False, "error": error.errors()}), 400

    raw_values = payload.model_dump()
    raw_frame = pd.DataFrame([raw_values])

    try:
        assets = get_model_assets()
        best_model_name = assets["metrics"]["best_model"]
        model_results = []

        for model_name, pipeline in assets["pipelines"].items():
            prediction_value = int(pipeline.predict(raw_frame)[0])
            default_probability = float(pipeline.predict_proba(raw_frame)[0, 1])
            model_results.append(
                {
                    "name": model_name,
                    "is_best_model": model_name == best_model_name,
                    "roc_auc": assets["metrics"]["models"][model_name]["roc_auc"],
                    "value": prediction_value,
                    "label": "Default" if prediction_value == 1 else "No Default",
                    "default_probability": default_probability,
                    "shap_explanation": get_shap_explanation(
                        model_name, pipeline, raw_frame, assets["backgrounds"][model_name]
                    ),
                }
            )

        best_result = next(item for item in model_results if item["is_best_model"])
        prediction_value = best_result["value"]
        default_probability = best_result["default_probability"]
        prediction_label = best_result["label"]
        best_pipeline = assets["pipelines"][best_model_name]
        model_features = best_pipeline.named_steps["feature_engineering"].transform(raw_frame).iloc[0]
    except FileNotFoundError as error:
        return jsonify({"success": False, "error": str(error)}), 503
    except (TypeError, ValueError) as error:
        return jsonify({"success": False, "error": str(error)}), 400

    record = PredictionRecord(
        **raw_values,
        Total_bill=float(model_features["Total_bill"]),
        Total_pay=float(model_features["Total_pay"]),
        Outstanding=float(model_features["Outstanding"]),
        prediction=prediction_value,
        prediction_label=prediction_label,
        default_probability=default_probability,
    )
    db.session.add(record)
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "prediction": {
                "value": prediction_value,
                "label": prediction_label,
                "default_probability": default_probability,
            },
            "best_model": best_model_name,
            "selection_metric": assets["metrics"]["selection_metric"],
            "models": model_results,
            "features": {
                key: float(model_features[key])
                for key in [
                    "LIMIT_BAL",
                    "AGE",
                    "PAY_0",
                    "BILL_AMT1",
                    "Total_bill",
                    "Total_pay",
                    "Outstanding",
                ]
            },
            "prediction_id": record.id,
        }
    ), 200
