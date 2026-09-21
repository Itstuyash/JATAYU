"""Pydantic schemas for API input validation."""

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Raw UCI fields required by the saved inference pipeline."""

    LIMIT_BAL: float = Field(..., gt=0, description="Credit limit must be greater than 0.")
    AGE: float = Field(..., gt=0, description="Age must be greater than 0.")
    PAY_0: float = Field(..., ge=0, le=8, description="PAY_0 must be between 0 and 8.")
    BILL_AMT1: float = Field(..., gt=0, description="Bill amount must be greater than 0.")
    BILL_AMT2: float = Field(..., gt=0, description="Bill amount must be greater than 0.")
    BILL_AMT3: float = Field(..., gt=0, description="Bill amount must be greater than 0.")
    BILL_AMT4: float = Field(..., gt=0, description="Bill amount must be greater than 0.")
    BILL_AMT5: float = Field(..., gt=0, description="Bill amount must be greater than 0.")
    BILL_AMT6: float = Field(..., gt=0, description="Bill amount must be greater than 0.")
    PAY_AMT1: float = Field(..., gt=0, description="Payment amount must be greater than 0.")
    PAY_AMT2: float = Field(..., gt=0, description="Payment amount must be greater than 0.")
    PAY_AMT3: float = Field(..., gt=0, description="Payment amount must be greater than 0.")
    PAY_AMT4: float = Field(..., gt=0, description="Payment amount must be greater than 0.")
    PAY_AMT5: float = Field(..., gt=0, description="Payment amount must be greater than 0.")
    PAY_AMT6: float = Field(..., gt=0, description="Payment amount must be greater than 0.")
    customer_code: str | None = None
