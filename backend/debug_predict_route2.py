import inspect
import pandas as pd

from app import create_app
from app.models import CustomerProfile
from app.routes.predict import predict
from ml.feature_engineering import transform_raw_input

app = create_app(reset_database=True)
print('source:')
print(inspect.getsource(predict))

with app.app_context():
    profile = CustomerProfile.query.filter_by(uci_id=23).first()
    raw = profile.to_raw_dict({'BILL_AMT1': 41087, 'PAY_AMT1': 2007})
    df = pd.DataFrame([raw])
    print('transform columns', transform_raw_input(df).columns.tolist())

with app.test_request_context('/api/predict', method='POST', json={'customer_id': 23, 'BILL_AMT1': 41087, 'PAY_AMT1': 2007}):
    response = predict()
    print('result type', type(response))
    print('result', response)
    if isinstance(response, tuple):
        print('status_code', response[1])
        print('body', response[0].get_data(as_text=True))
