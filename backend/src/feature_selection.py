from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, mutual_info_classif

from src.config import EXCLUDED_FEATURES, FEATURE_IMPORTANCE_FILE, FEATURE_RANKINGS_FILE, SELECTED_FEATURES_FILE
from src.utils import save_joblib_artifact


@dataclass
class FeatureSelectionResult:
    selected_features: list[str]
    rankings: pd.DataFrame


def rank_features(frame: pd.DataFrame, target_column: str = "label", top_k: int | None = None) -> FeatureSelectionResult:
    working = frame.copy()
    feature_columns = [
        column
        for column in working.columns
        if column not in {target_column, "url"} and column not in EXCLUDED_FEATURES
    ]

    numeric_features = working[feature_columns].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    target = working[target_column].astype(int)

    correlation_values = []
    for column in feature_columns:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            correlation_values.append(abs(numeric_features[column].corr(target)))
    correlations = pd.Series(correlation_values, index=feature_columns).replace([np.inf, -np.inf], np.nan).fillna(0.0)

    forest = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")
    forest.fit(numeric_features, target)

    selector = SelectKBest(score_func=mutual_info_classif, k=min(20, len(feature_columns)))
    selector.fit(numeric_features, target)
    mi_scores = pd.Series(selector.scores_, index=feature_columns).fillna(0.0)

    rankings = pd.DataFrame(
        {
            "feature": feature_columns,
            "abs_correlation": correlations.values,
            "random_forest_importance": forest.feature_importances_,
            "mutual_information": mi_scores.values,
        }
    ).sort_values(
        by=["random_forest_importance", "mutual_information", "abs_correlation"],
        ascending=False,
    )

    if top_k is None:
        top_k = min(20, len(rankings))
    selected_features = rankings.head(top_k)["feature"].tolist()
    return FeatureSelectionResult(selected_features=selected_features, rankings=rankings)


def save_feature_selection(result: FeatureSelectionResult) -> None:
    FEATURE_RANKINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.rankings.to_csv(FEATURE_RANKINGS_FILE, index=False)
    save_joblib_artifact(result.selected_features, SELECTED_FEATURES_FILE)


def plot_feature_importance(result: FeatureSelectionResult, output_path: Path = FEATURE_IMPORTANCE_FILE) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    chart = result.rankings.head(15).sort_values("random_forest_importance")
    plt.figure(figsize=(10, 6))
    plt.barh(chart["feature"], chart["random_forest_importance"], color="#00d1b2")
    plt.title("Feature Importance Ranking")
    plt.xlabel("Random Forest Importance")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
