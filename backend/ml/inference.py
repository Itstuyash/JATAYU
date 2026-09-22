"""Inference helpers for pipeline-based model diagnostics."""


def transform_for_classifier(pipeline, X):
    """Apply the pipeline’s preprocessing stage when present."""
    feature_engineering = pipeline.named_steps.get("feature_engineering")
    if feature_engineering is not None:
        return feature_engineering.transform(X)
    return X
