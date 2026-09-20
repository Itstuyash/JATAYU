"""Reusable feature engineering for credit-card default predictions."""

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


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


class CreditCardFeatureEngineer(BaseEstimator, TransformerMixin):
    """Create model features from the raw fields submitted by a client.

    The transformer performs the same work during training and inference, so
    Flask never needs to reproduce the feature-engineering logic itself.
    """

    def fit(self, X, y=None):
        """Validate the training columns and return the fitted transformer."""
        self._validate_columns(X)
        return self

    def transform(self, X):
        """Return the seven final model features as a DataFrame."""
        self._validate_columns(X)
        data = X.copy()

        data["Total_bill"] = data[BILL_COLUMNS].sum(axis=1)
        data["Total_pay"] = data[PAYMENT_COLUMNS].sum(axis=1)
        data["Outstanding"] = data["Total_bill"] - data["Total_pay"]

        return data.loc[:, MODEL_FEATURES]

    @staticmethod
    def _validate_columns(X):
        if not isinstance(X, pd.DataFrame):
            raise TypeError("Prediction input must be a pandas DataFrame.")

        missing_columns = sorted(set(RAW_REQUIRED_COLUMNS) - set(X.columns))
        if missing_columns:
            raise ValueError(
                "Missing required raw input columns: " + ", ".join(missing_columns)
            )
