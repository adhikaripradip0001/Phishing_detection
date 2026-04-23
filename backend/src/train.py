from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

from src.config import BEST_MODEL_FILE, LABEL_ENCODER_FILE, MODEL_SEARCH_SPACE, RANDOM_STATE, SCALER_FILE, TRAINING_LOG_FILE, VALIDATION_CV
from src.evaluate import evaluate_predictions
from src.preprocessing import TabularPreprocessor, prepare_training_features
from src.utils import save_joblib_artifact, setup_logger

try:
    XGBClassifier = import_module("xgboost").XGBClassifier
except Exception:  # pragma: no cover - optional dependency
    XGBClassifier = None


LOGGER = setup_logger("training", TRAINING_LOG_FILE)


@dataclass
class TrainingResult:
    model_name: str
    estimator: object
    preprocessor: TabularPreprocessor
    label_encoder: LabelEncoder
    comparison: pd.DataFrame
    metrics: dict[str, float]
    feature_names: list[str]


def _candidate_models() -> dict[str, tuple[object, dict[str, list[object]]]]:
    models: dict[str, tuple[object, dict[str, list[object]]]] = {
        "Decision Tree": (DecisionTreeClassifier(random_state=RANDOM_STATE, class_weight="balanced"), MODEL_SEARCH_SPACE["decision_tree"]),
        "Random Forest": (RandomForestClassifier(random_state=RANDOM_STATE, class_weight="balanced"), MODEL_SEARCH_SPACE["random_forest"]),
        "SVM": (SVC(probability=True, random_state=RANDOM_STATE), MODEL_SEARCH_SPACE["svm"]),
        "Logistic Regression": (
            LogisticRegression(max_iter=2000, class_weight="balanced", random_state=RANDOM_STATE),
            {"model__C": [0.1, 1.0, 5.0, 10.0]},
        ),
    }
    if XGBClassifier is not None:
        models["XGBoost"] = (
            XGBClassifier(
                random_state=RANDOM_STATE,
                n_estimators=150,
                eval_metric="logloss",
                tree_method="hist",
            ),
            {"model__max_depth": [3, 5, 7], "model__learning_rate": [0.05, 0.1], "model__subsample": [0.8, 1.0]},
        )
    return models


def train_models(train_dataset: pd.DataFrame, test_dataset: pd.DataFrame) -> TrainingResult:
    working_train = train_dataset.copy()
    working_test = test_dataset.copy()
    if "label" not in working_train.columns or "label" not in working_test.columns:
        raise ValueError("Training dataset must include a label column.")

    train_features, train_target = prepare_training_features(working_train)
    test_features, test_target = prepare_training_features(working_test)
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(train_target.map({0: "legitimate", 1: "phishing"}))
    y_test = label_encoder.transform(test_target.map({0: "legitimate", 1: "phishing"}))

    preprocessor = TabularPreprocessor().fit(train_features)
    X_train_scaled = preprocessor.transform(train_features)
    X_test_scaled = preprocessor.transform(test_features)

    comparison_rows: list[dict[str, float | str]] = []
    best_estimator = None
    best_model_name = ""
    best_score = -np.inf
    best_metrics: dict[str, float] = {}

    for model_name, (model, param_grid) in _candidate_models().items():
        pipeline = Pipeline([("model", clone(model))])
        search = GridSearchCV(
            pipeline,
            param_grid=param_grid,
            scoring="f1",
            cv=StratifiedKFold(n_splits=VALIDATION_CV, shuffle=True, random_state=RANDOM_STATE),
            n_jobs=-1,
            refit=True,
        )
        search.fit(X_train_scaled, y_train)
        estimator = search.best_estimator_
        predictions = estimator.predict(X_test_scaled)
        probabilities = estimator.predict_proba(X_test_scaled)[:, 1] if hasattr(estimator, "predict_proba") else None
        metrics = evaluate_predictions(y_test, predictions, probabilities)

        comparison_rows.append(
            {
                "model": model_name,
                "cv_f1": float(search.best_score_),
                "accuracy": metrics["accuracy"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1_score": metrics["f1_score"],
                "roc_auc": metrics.get("roc_auc", np.nan),
            }
        )

        LOGGER.info("%s | best cv f1=%.4f | test f1=%.4f", model_name, search.best_score_, metrics["f1_score"])
        if metrics["f1_score"] > best_score:
            best_score = metrics["f1_score"]
            best_estimator = estimator
            best_model_name = model_name
            best_metrics = metrics

    comparison = pd.DataFrame(comparison_rows).sort_values("f1_score", ascending=False).reset_index(drop=True)
    if best_estimator is None:
        raise RuntimeError("No model could be trained successfully.")

    save_joblib_artifact(best_estimator, BEST_MODEL_FILE)
    save_joblib_artifact(preprocessor, SCALER_FILE)
    save_joblib_artifact(label_encoder, LABEL_ENCODER_FILE)

    return TrainingResult(
        model_name=best_model_name,
        estimator=best_estimator,
        preprocessor=preprocessor,
        label_encoder=label_encoder,
        comparison=comparison,
        metrics=best_metrics,
        feature_names=preprocessor.feature_names,
    )
