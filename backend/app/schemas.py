from  pydantic import BaseModel, Field

class LivePredictionSchema(BaseModel):
    age: float=Field(gt=18,lt=100)
    income: float=Field(gt=0)
    loan: float=Field(gt=0)
    loan_to_income_ratio: float=Field(gt=0,lt=1)