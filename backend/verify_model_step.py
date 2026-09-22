import pandas as pd

from app import create_app
from app.models import CustomerProfile
import app.routes.predict as route_mod

app = create_app(reset_database=True)
route_mod.get_model_assets.cache_clear()

with app.app_context():
    profile = CustomerProfile.query.filter_by(uci_id=23).first()
    raw = profile.to_raw_dict({'BILL_AMT1': 41087, 'PAY_AMT1': 2007})
    df = pd.DataFrame([raw])
    print('raw_missing', [c for c in ['LIMIT_BAL','AGE','PAY_0','BILL_AMT1','BILL_AMT2','BILL_AMT3','BILL_AMT4','BILL_AMT5','BILL_AMT6','PAY_AMT1','PAY_AMT2','PAY_AMT3','PAY_AMT4','PAY_AMT5','PAY_AMT6'] if c not in df.columns])
    transformed = route_mod.transform_raw_input(df)
    print('transformed_columns', transformed.columns.tolist())
    assets = route_mod.get_model_assets()
    print('artifact_keys', sorted(assets.keys()))
    print('pipelines', list(assets['pipelines'].keys()))
    for name, pipeline in assets['pipelines'].items():
        proba = float(pipeline.predict_proba(transformed)[0, 1])
        print(name, proba)
