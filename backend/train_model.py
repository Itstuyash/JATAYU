"""Train and save the complete credit-card default prediction pipeline."""

from pathlib import Path
import json

import joblib
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from ml.feature_engineering import CreditCardFeatureEngineer
from ml.inference import transform_for_classifier


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "data" / "UCI_Credit_Card.xls"
PIPELINE_PATH = BASE_DIR / "ml" / "credit_card_default_pipeline.pkl"
MODEL_PATHS = {
    "Random Forest": PIPELINE_PATH,
    "Logistic Regression": BASE_DIR / "ml" / "logistic_regression_pipeline.pkl",
    "XGBoost": BASE_DIR / "ml" / "xgboost_pipeline.pkl",
}
METRICS_PATH = BASE_DIR / "ml" / "model_metrics.json"
SHAP_BACKGROUNDS_PATH = BASE_DIR / "ml" / "shap_backgrounds.pkl"
TARGET_COLUMN = "default.payment.next.month"


def load_dataset(dataset_path=DATASET_PATH):
    """Load the UCI dataset and validate its required columns."""
    data = pd.read_excel(dataset_path, header=1)

    # The original UCI Excel file spells the target with spaces. Normalize it
    # once at the data boundary to the project's canonical target name.
    data = data.rename(columns={"default payment next month": TARGET_COLUMN})

    required_columns = {"ID", TARGET_COLUMN}
    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError("Dataset is missing columns: " + ", ".join(sorted(missing_columns)))
    return data


def build_pipeline(classifier, use_scaler=False):
    """Build a complete inference pipeline for one classifier."""
    steps = [
        ("feature_engineering", CreditCardFeatureEngineer()),
        ("smote", SMOTE(random_state=42)),
    ]
    if use_scaler:
        steps.append(("scaler", StandardScaler()))
    steps.append(("classifier", classifier))
    return Pipeline(steps=steps)


def build_model_pipelines():
    """Create the three models using the parameters from the supplied notebooks."""
    return {
        "Random Forest": build_pipeline(
            RandomForestClassifier(n_estimators=250, random_state=42, n_jobs=-1)
        ),
        "Logistic Regression": build_pipeline(
            LogisticRegression(random_state=42, max_iter=5000), use_scaler=True
        ),
        "XGBoost": build_pipeline(
            XGBClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=4,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                n_jobs=-1,
                eval_metric="logloss",
            ),
            use_scaler=True,
        ),
    }


def main():
    """Train, evaluate, and save the complete pipeline."""
    data = load_dataset()
    X = data.drop(columns=["ID", TARGET_COLUMN])
    y = data[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    metrics = {}
    shap_backgrounds = {}
    for model_name, pipeline in build_model_pipelines().items():
        pipeline.fit(X_train, y_train)
        test_predictions = pipeline.predict(X_test)
        test_probabilities = pipeline.predict_proba(X_test)[:, 1]
        metrics[model_name] = {
            "accuracy": round(float(accuracy_score(y_test, test_predictions)), 6),
            "roc_auc": round(float(roc_auc_score(y_test, test_probabilities)), 6),
        }
        print(f"\n{model_name}")
        print(f"Test accuracy: {metrics[model_name]['accuracy']:.4f}")
        print(f"Test ROC-AUC: {metrics[model_name]['roc_auc']:.4f}")
        print(classification_report(y_test, test_predictions))

        joblib.dump(pipeline, MODEL_PATHS[model_name])
        engineered_background = pipeline.named_steps["feature_engineering"].transform(X_train)
        shap_backgrounds[model_name] = transform_for_classifier(
            pipeline, X_train.sample(n=min(100, len(X_train)), random_state=42)
        )

    best_model = max(metrics, key=lambda name: metrics[name]["roc_auc"])
    with METRICS_PATH.open("w", encoding="utf-8") as metrics_file:
        json.dump({"selection_metric": "roc_auc", "best_model": best_model, "models": metrics}, metrics_file, indent=2)
    joblib.dump(shap_backgrounds, SHAP_BACKGROUNDS_PATH)
    print(f"\nBest model by ROC-AUC: {best_model}")
    print(f"Saved model metrics to: {METRICS_PATH}")


if __name__ == "__main__":
    main()
