"""Pydantic schemas for API input validation."""

from pydantic import BaseModel


class PredictionRequest(BaseModel):
    """Raw UCI fields required by the saved inference pipeline."""

    LIMIT_BAL: float
    AGE: float
    PAY_0: float
    BILL_AMT1: float
    BILL_AMT2: float
    BILL_AMT3: float
    BILL_AMT4: float
    BILL_AMT5: float
    BILL_AMT6: float
    PAY_AMT1: float
    PAY_AMT2: float
    PAY_AMT3: float
    PAY_AMT4: float
    PAY_AMT5: float
    PAY_AMT6: float
    customer_code: str | None = None
