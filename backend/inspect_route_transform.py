import pandas as pd

from app import create_app
import app.routes.predict as route_mod
from app.models import CustomerProfile

app = create_app(reset_database=True)

original = route_mod.transform_raw_input

def wrapper(df):
    print('wrapped df columns', df.columns.tolist())
    print('wrapped missing', [c for c in ['LIMIT_BAL', 'AGE', 'PAY_0', 'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6'] if c not in df.columns])
    result = original(df)
    print('wrapped result columns', result.columns.tolist())
    return result

route_mod.transform_raw_input = wrapper

with app.app_context():
    profile = CustomerProfile.query.filter_by(uci_id=23).first()
    raw = profile.to_raw_dict({'BILL_AMT1': 41087, 'PAY_AMT1': 2007})
    print('raw keys', sorted(raw.keys()))
    print('std check', original(pd.DataFrame([raw])).columns.tolist())

with app.test_request_context('/api/predict', method='POST', json={'customer_id': 23, 'BILL_AMT1': 41087, 'PAY_AMT1': 2007}):
    response = route_mod.predict()
    print('response', response)
