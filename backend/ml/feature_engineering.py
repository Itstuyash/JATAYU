"""Notebook-compatible preprocessing for credit-card default models."""

from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


RAW_REQUIRED_COLUMNS = [
    "LIMIT_BAL",
    "AGE",
    "PAY_0",
    "BILL_AMT1",
    "BILL_AMT2",
    "BILL_AMT3",
    "BILL_AMT4",
    "BILL_AMT5",
    "BILL_AMT6",
    "PAY_AMT1",
    "PAY_AMT2",
    "PAY_AMT3",
    "PAY_AMT4",
    "PAY_AMT5",
    "PAY_AMT6",
]

MODEL_FEATURES = [
    "LIMIT_BAL",
    "AGE",
    "PAY_0",
    "BILL_AMT1",
    "Total_bill",
    "Total_pay",
    "Outstanding",
]

BILL_COLUMNS = [f"BILL_AMT{month}" for month in range(1, 7)]
PAYMENT_COLUMNS = [f"PAY_AMT{month}" for month in range(1, 7)]
REPAYMENT_COLUMNS = ["PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]
DROPPED_NOTEBOOK_COLUMNS = [
    "PAY_2",
    "PAY_3",
    "PAY_4",
    "PAY_5",
    "PAY_6",
    "BILL_AMT2",
    "BILL_AMT3",
    "BILL_AMT4",
    "BILL_AMT5",
    "BILL_AMT6",
]


class CreditCardFeatureEngineer(BaseEstimator, TransformerMixin):
    """Apply the notebook's raw-data cleaning and feature reduction."""

    def fit(self, X, y=None):
        self._validate_columns(X)
        return self

    def transform(self, X):
        self._validate_columns(X)
        data = X.copy()

        if "EDUCATION" in data.columns:
            data.loc[data["EDUCATION"].isin([0, 6]), "EDUCATION"] = 5
        if "MARRIAGE" in data.columns:
            data.loc[data["MARRIAGE"] == 0, "MARRIAGE"] = 3

        for column in REPAYMENT_COLUMNS:
            if column in data.columns:
                data.loc[data[column].isin([-1, -2]), column] = 0

        for column in BILL_COLUMNS:
            data[column] = data[column].abs()

        data["Total_bill"] = data[BILL_COLUMNS].sum(axis=1)
        data["Total_pay"] = data[PAYMENT_COLUMNS].sum(axis=1)
        data["Outstanding"] = data["Total_bill"] - data["Total_pay"]

        data = data.drop(columns=DROPPED_NOTEBOOK_COLUMNS, errors="ignore")
        return data.loc[:, MODEL_FEATURES]

    @staticmethod
    def _validate_columns(X):
        if not isinstance(X, pd.DataFrame):
            raise TypeError("Prediction input must be a pandas DataFrame.")

        missing_columns = [
            column for column in RAW_REQUIRED_COLUMNS if column not in X.columns
        ]
        if missing_columns:
            raise ValueError(
                "Missing required raw input columns: " + ", ".join(missing_columns)
            )


def transform_raw_input(raw_frame):
    """Transform raw backend fields into the seven pickle-model features."""
    return CreditCardFeatureEngineer().fit_transform(raw_frame)
