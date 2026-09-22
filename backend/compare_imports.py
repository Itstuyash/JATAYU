import pandas as pd
from app import create_app
from app.models import CustomerProfile
from app.routes import predict as route_mod
from ml.feature_engineering import transform_raw_input as direct_transform

app = create_app(reset_database=True)
with app.app_context():
    profile = CustomerProfile.query.filter_by(uci_id=23).first()
    raw = profile.to_raw_dict({'BILL_AMT1': 41087, 'PAY_AMT1': 2007})
    df = pd.DataFrame([raw])
    direct_result = direct_transform(df)
    route_result = route_mod.transform_raw_input(df)
    print('same object', direct_transform is route_mod.transform_raw_input)
    print('direct columns', direct_result.columns.tolist())
    print('route columns', route_result.columns.tolist())
    print('module', route_mod.__file__)
