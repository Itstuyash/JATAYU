from pathlib import Path
import pickle

import pandas as pd
from flask import Blueprint, request, jsonify


predict_bp = Blueprint("predict", __name__)


BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "ml" / "model.pkl"


with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


@predict_bp.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    input_data = pd.DataFrame([data])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0].max()

    return jsonify({
        "prediction": int(prediction),
        "confidence": float(probability)
    })