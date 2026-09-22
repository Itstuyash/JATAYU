from app import create_app
from app.routes.predict import predict

app = create_app(reset_database=True)
with app.test_request_context('/api/predict', method='POST', json={'customer_id': 23, 'BILL_AMT1': 41087, 'PAY_AMT1': 2007}):
    resp = predict()
    print('type', type(resp))
    if isinstance(resp, tuple):
        print('status', resp[1])
        print('body', resp[0].get_data(as_text=True))
    else:
        print('data', resp.get_data(as_text=True))
        print('status', resp.status_code)
