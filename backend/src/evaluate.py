from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    auc,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split

from src.config import BEST_MODEL_FILE, RANDOM_STATE, SCALER_FILE, SELECTED_FEATURES_DATASET_FILE, TEST_SIZE
from src.preprocessing import TabularPreprocessor, prepare_training_features
from src.utils import load_joblib_artifact

from src.config import CONFUSION_MATRIX_FILE, EVALUATION_REPORT_FILE, MODEL_COMPARISON_CSV_FILE, MODEL_COMPARISON_FILE, ROC_CURVE_FILE
from src.utils import write_text_file


def evaluate_predictions(y_true, y_pred, y_proba=None) -> dict[str, float]:
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1_score": f1_score(y_true, y_pred, zero_division=0),
    }
    if y_proba is not None:
        fpr, tpr, _ = roc_curve(y_true, y_proba)
        metrics["roc_auc"] = auc(fpr, tpr)
    return metrics


def plot_confusion_matrix(y_true, y_pred, output_path: Path = CONFUSION_MATRIX_FILE) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    matrix = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(5, 4))
    plt.imshow(matrix, interpolation="nearest", cmap="Blues")
    plt.title("Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ["Legitimate", "Phishing"], rotation=20)
    plt.yticks(tick_marks, ["Legitimate", "Phishing"])
    threshold = matrix.max() / 2.0 if matrix.max() else 0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            plt.text(j, i, format(matrix[i, j], "d"), ha="center", va="center", color="white" if matrix[i, j] > threshold else "black")
    plt.ylabel("Actual")
    plt.xlabel("Predicted")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_roc_curve(y_true, y_proba, output_path: Path = ROC_CURVE_FILE) -> None:
    if y_proba is None:
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    curve_auc = auc(fpr, tpr)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, label=f"ROC AUC = {curve_auc:.3f}", color="#ff6b6b")
    plt.plot([0, 1], [0, 1], linestyle="--", color="#666666")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_model_comparison(comparison: pd.DataFrame, output_path: Path = MODEL_COMPARISON_FILE) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    chart = comparison.sort_values("f1_score", ascending=True)
    plt.figure(figsize=(10, 6))
    plt.barh(chart["model"], chart["f1_score"], color="#00c2ff")
    plt.xlabel("F1-score")
    plt.title("Model Comparison")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def write_evaluation_report(comparison: pd.DataFrame, best_model_name: str, metrics: dict[str, float]) -> None:
    lines = ["AI-Based Phishing Website Detection System Evaluation", "", f"Best Model: {best_model_name}", ""]
    for key, value in metrics.items():
        lines.append(f"{key}: {value:.4f}")
    lines.extend(["", "Model Comparison:", comparison.to_string(index=False)])
    write_text_file(EVALUATION_REPORT_FILE, "\n".join(lines))


def save_model_comparison_csv(comparison: pd.DataFrame) -> None:
    MODEL_COMPARISON_CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(MODEL_COMPARISON_CSV_FILE, index=False)


def evaluate_saved_model(dataset: pd.DataFrame | None = None, split_data: bool = True) -> tuple[pd.DataFrame, dict[str, float], str]:
    if dataset is None:
        dataset = pd.read_csv(SELECTED_FEATURES_DATASET_FILE)

    model = load_joblib_artifact(BEST_MODEL_FILE)
    preprocessor = load_joblib_artifact(SCALER_FILE)
    if model is None or preprocessor is None:
        raise RuntimeError("Saved model artifacts were not found. Train the system first.")

    features, target = prepare_training_features(dataset)
    target_encoded = target.astype(int).to_numpy()

    if split_data:
        _, X_test, _, y_test = train_test_split(
            features,
            target_encoded,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=target_encoded,
        )
    else:
        X_test = features
        y_test = target_encoded

    if not isinstance(preprocessor, TabularPreprocessor):
        raise TypeError("Loaded preprocessor artifact is invalid.")

    transformed = preprocessor.transform(X_test)
    predictions = model.predict(transformed)
    probabilities = model.predict_proba(transformed)[:, 1] if hasattr(model, "predict_proba") else None
    metrics = evaluate_predictions(y_test, predictions, probabilities)

    model_name = type(model.named_steps["model"]).__name__ if hasattr(model, "named_steps") and "model" in model.named_steps else type(model).__name__
    comparison = pd.DataFrame(
        [
            {
                "model": model_name,
                "cv_f1": np.nan,
                "accuracy": metrics["accuracy"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1_score": metrics["f1_score"],
                "roc_auc": metrics.get("roc_auc", np.nan),
            }
        ]
    )

    plot_confusion_matrix(y_test, predictions)
    plot_roc_curve(y_test, probabilities)
    plot_model_comparison(comparison)
    save_model_comparison_csv(comparison)
    write_evaluation_report(comparison, model_name, metrics)
    return comparison, metrics, model_name
