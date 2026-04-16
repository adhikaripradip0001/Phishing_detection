from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from src.config import BEST_MODEL_FILE, LABEL_ENCODER_FILE, SCALER_FILE, SELECTED_FEATURES_FILE
from src.feature_engineering import build_feature_row
from src.legacy_feature_adapter import adapt_features_for_selected_schema
from src.preprocessing import TabularPreprocessor
from src.utils import load_joblib_artifact


def _load_bundle():
    model = load_joblib_artifact(BEST_MODEL_FILE)
    preprocessor = load_joblib_artifact(SCALER_FILE)
    label_encoder = load_joblib_artifact(LABEL_ENCODER_FILE)
    selected_features = load_joblib_artifact(SELECTED_FEATURES_FILE, default=[])
    return model, preprocessor, label_encoder, selected_features


def predict_single_url(url: str, include_content: bool = True) -> dict[str, object]:
    model, preprocessor, label_encoder, selected_features = _load_bundle()
    if model is None or preprocessor is None:
        return {
            "success": False,
            "error": "Trained model artifacts were not found. Run training first.",
        }

    if not isinstance(preprocessor, TabularPreprocessor):
        raise TypeError("Loaded preprocessor artifact is invalid.")

    feature_row = build_feature_row(url, include_content=include_content)
    schema_mode = "native"
    if selected_features:
        missing_before = [feature for feature in selected_features if feature not in feature_row]
        feature_row = adapt_features_for_selected_schema(url, feature_row, selected_features)
        missing_after = [feature for feature in selected_features if feature not in feature_row]
        if missing_before and len(missing_after) < len(missing_before):
            schema_mode = "legacy_mapped"
        elif missing_before:
            schema_mode = "partial_mapped"
    feature_frame = pd.DataFrame([feature_row])

    if selected_features:
        for feature in selected_features:
            if feature not in feature_frame.columns:
                feature_frame[feature] = 0
        feature_frame = feature_frame[selected_features]

    transformed = preprocessor.transform(feature_frame)
    prediction = int(model.predict(transformed)[0])
    proba = float(model.predict_proba(transformed)[0][1]) if hasattr(model, "predict_proba") else float(1.0 / (1.0 + np.exp(-model.decision_function(transformed)[0])))

    risk_signals: list[str] = []
    if int(feature_row.get("looks_like_brand_typo", 0)) == 1:
        risk_signals.append("brand_typosquatting_pattern")
        proba = max(proba, 0.85)
        prediction = 1

    label = "phishing" if prediction == 1 else "legitimate"
    if isinstance(label_encoder, LabelEncoder):
        class_label = label_encoder.inverse_transform([prediction])[0]
    else:
        class_label = label

    return {
        "success": True,
        "url": url,
        "predicted_label": label,
        "encoded_label": int(prediction),
        "class_label": class_label,
        "schema_mode": schema_mode,
        "phishing_probability": round(proba, 4),
        "confidence": round(max(proba, 1 - proba), 4),
        "warning": "Potential phishing risk detected." if prediction == 1 else "No immediate phishing indicators detected.",
        "risk_signals": risk_signals,
        "key_features": {
            key: feature_row.get(key)
            for key in [
                "url_length",
                "domain_length",
                "path_length",
                "num_dots",
                "num_hyphens",
                "has_ip_address",
                "uses_https",
                "suspicious_keyword_count",
                "looks_like_brand_typo",
                "brand_similarity_score",
                "domain_age_days",
                "domain_expiry_days",
                "num_forms",
                "num_input_fields",
                "has_password_field",
                "num_external_links",
                "num_internal_links",
                "has_iframe",
                "has_js_redirect",
            ]
            if key in feature_row
        },
        "all_features": feature_row,
    }
