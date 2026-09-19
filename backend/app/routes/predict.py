from pathlib import Path
import pickle

from ..models import LivePrediction, db
from ..schemas import LivePredictionSchema

import pandas as pd
from flask import Blueprint, request, jsonify


predict_bp = Blueprint("predict", __name__)


BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "ml" / "model.pkl"


with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


def normalize_prediction_payload(data):
    if not isinstance(data, dict):
        return {}

    normalized = {}
    for key, value in data.items():
        if key is None:
            continue

        key_name = str(key).strip().lower().replace("-", "_").replace(" ", "_")
        aliases = {
            "age": "age",
            "income": "income",
            "loan": "loan",
            "loan_to_income": "loan_to_income_ratio",
            "loan_to_income_ratio": "loan_to_income_ratio",
            "loan_to_income_percentage": "loan_to_income_ratio",
        }
        normalized[aliases.get(key_name, key_name)] = value

    return normalized


@predict_bp.route("/predict", methods=["POST"])
def predict():

    data = request.get_json(silent=True) or {}
    normalized_data = normalize_prediction_payload(data)

    try:
        validated_data = LivePredictionSchema(**normalized_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    input_data = pd.DataFrame([validated_data.model_dump()])
    input_data = input_data.rename(columns={
        "age": "Age",
        "income": "Income",
        "loan": "Loan",
        "loan_to_income_ratio": "Loan to Income"
    })
    input_data = input_data.reindex(columns=list(model.feature_names_in_))

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0].max()

    db_entry = LivePrediction(
        age=validated_data.age,
        income=validated_data.income,
        loan=validated_data.loan,
        loan_to_income_ratio=validated_data.loan_to_income_ratio,
        prediction=int(prediction)
    )

    db.session.add(db_entry)
    db.session.commit()

    return jsonify({
        "prediction": int(prediction),
        "confidence": float(probability)
    })