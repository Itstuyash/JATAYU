from app import create_app
from app.models import CustomerProfile
from app.schemas import PredictionRequest
from app.routes.predict import predict
from flask import request

app = create_app(reset_database=True)
with app.app_context():
    profile = CustomerProfile.query.filter_by(uci_id=23).first()
    payload = PredictionRequest.model_validate({'customer_id': 23, 'BILL_AMT1': 41087, 'PAY_AMT1': 2007})
    raw_values = profile.to_raw_dict({'BILL_AMT1': float(payload.BILL_AMT1), 'PAY_AMT1': float(payload.PAY_AMT1)})
    print('raw keys', sorted(raw_values.keys()))
    print('has all', all(k in raw_values for k in ['LIMIT_BAL','AGE','PAY_0','BILL_AMT1','BILL_AMT2','BILL_AMT3','BILL_AMT4','BILL_AMT5','BILL_AMT6','PAY_AMT1','PAY_AMT2','PAY_AMT3','PAY_AMT4','PAY_AMT5','PAY_AMT6']))
    print('raw sample', raw_values)

    with app.test_request_context('/api/predict', method='POST', json={'customer_id': 23, 'BILL_AMT1': 41087, 'PAY_AMT1': 2007}):
        payload2 = PredictionRequest.model_validate(request.get_json(silent=True))
        profile2 = CustomerProfile.query.filter_by(uci_id=payload2.customer_id).first()
        raw_values2 = profile2.to_raw_dict({'BILL_AMT1': float(payload2.BILL_AMT1), 'PAY_AMT1': float(payload2.PAY_AMT1)})
        print('raw2 keys', sorted(raw_values2.keys()))
        print('all2', all(k in raw_values2 for k in ['LIMIT_BAL','AGE','PAY_0','BILL_AMT1','BILL_AMT2','BILL_AMT3','BILL_AMT4','BILL_AMT5','BILL_AMT6','PAY_AMT1','PAY_AMT2','PAY_AMT3','PAY_AMT4','PAY_AMT5','PAY_AMT6']))
        from ml.feature_engineering import transform_raw_input
        import pandas as pd
        df = pd.DataFrame([raw_values2])
        print(df.columns.tolist())
        print(transform_raw_input(df).columns.tolist())
        resp = predict()
        print('route response', resp)
