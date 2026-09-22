import pandas as pd

from app import create_app
from app.models import CustomerProfile
from ml.feature_engineering import transform_raw_input

app = create_app(reset_database=True)
with app.app_context():
    profile = CustomerProfile.query.filter_by(uci_id=23).first()
    print('profile_exists', bool(profile))
    if not profile:
        raise SystemExit('Customer 23 not found after rebuilding profile table')
    raw = profile.to_raw_dict({'BILL_AMT1': 41087, 'PAY_AMT1': 2007})
    missing = [
        c for c in [
            'LIMIT_BAL','AGE','PAY_0','BILL_AMT1','BILL_AMT2','BILL_AMT3','BILL_AMT4','BILL_AMT5','BILL_AMT6',
            'PAY_AMT1','PAY_AMT2','PAY_AMT3','PAY_AMT4','PAY_AMT5','PAY_AMT6'
        ]
        if c not in raw
    ]
    print('missing_columns', missing)
    if missing:
        raise SystemExit(f'Missing columns after rebuild: {missing}')

    df = pd.DataFrame([raw])
    transformed = transform_raw_input(df)
    print('transformed columns', transformed.columns.tolist())
    print('transformed values', transformed.to_dict(orient='records')[0])

    client = app.test_client()
    response = client.post('/api/predict', json={'customer_id': 23, 'BILL_AMT1': 41087, 'PAY_AMT1': 2007})
    print('status', response.status_code)
    print(response.get_data(as_text=True)[:500])
