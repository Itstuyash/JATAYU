"""Helpers that prepare raw input through a saved model pipeline."""


def transform_for_classifier(pipeline, raw_frame):
    """Use the saved pipeline steps to prepare one raw input for its classifier."""
    engineered = pipeline.named_steps["feature_engineering"].transform(raw_frame)
    scaler = pipeline.named_steps.get("scaler")
    return engineered if scaler is None else scaler.transform(engineered)
