"""Pydantic schemas for API input validation."""

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Current-month values used with an imported UCI customer profile."""

    customer_id: int = Field(..., gt=0, description="The UCI customer ID.")
    BILL_AMT1: float = Field(..., gt=0, description="Bill amount must be greater than 0.")
    PAY_AMT1: float = Field(..., gt=0, description="Payment amount must be greater than 0.")
