"""Independently load and test the saved credit-card default pipeline."""

from pathlib import Path

import joblib
import pandas as pd


PIPELINE_PATH = Path(__file__).resolve().parent / "ml" / "credit_card_default_pipeline.pkl"

SAMPLE_CUSTOMER = {
    "LIMIT_BAL": 200000,
    "AGE": 40,
    "PAY_0": 2,
    "BILL_AMT1": 15500,
    "BILL_AMT2": 12000,
    "BILL_AMT3": 11000,
    "BILL_AMT4": 10000,
    "BILL_AMT5": 9000,
    "BILL_AMT6": 10000,
    "PAY_AMT1": 8000,
    "PAY_AMT2": 7000,
    "PAY_AMT3": 6000,
    "PAY_AMT4": 5000,
    "PAY_AMT5": 6000,
    "PAY_AMT6": 6000,
}


def main():
    """Load the pickle and run one raw-input prediction."""
    pipeline = joblib.load(PIPELINE_PATH)
    customer = pd.DataFrame([SAMPLE_CUSTOMER])
    prediction = int(pipeline.predict(customer)[0])
    default_probability = float(pipeline.predict_proba(customer)[0, 1])

    print(f"Prediction: {prediction}")
    print(f"Default probability: {default_probability:.4f}")


if __name__ == "__main__":
    main()
