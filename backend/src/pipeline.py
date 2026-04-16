from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import (
    CLEANED_DATASET_FILE,
    FEATURED_DATASET_FILE,
    SELECTED_FEATURES_DATASET_FILE,
)
from src.data_cleaning import clean_raw_dataset
from src.data_loader import load_phishing_and_legitimate_data, load_raw_dataset, save_raw_dataset
from src.evaluate import plot_model_comparison, save_model_comparison_csv, write_evaluation_report
from src.feature_engineering import build_feature_dataset
from src.feature_selection import FeatureSelectionResult, plot_feature_importance, rank_features, save_feature_selection
from src.train import TrainingResult, train_models


def prepare_datasets(include_content: bool = True, raw_dataset_path: Path | None = None) -> pd.DataFrame:
    raw = load_raw_dataset(raw_dataset_path) if raw_dataset_path else load_phishing_and_legitimate_data()
    save_raw_dataset(raw)

    # If no URL column exists, dataset is already feature-engineered.
    if "url" not in raw.columns and "label" in raw.columns:
        featured = raw.dropna(subset=["label"]).drop_duplicates().reset_index(drop=True)
        CLEANED_DATASET_FILE.parent.mkdir(parents=True, exist_ok=True)
        featured.to_csv(CLEANED_DATASET_FILE, index=False)
        FEATURED_DATASET_FILE.parent.mkdir(parents=True, exist_ok=True)
        featured.to_csv(FEATURED_DATASET_FILE, index=False)
        return featured

    cleaned = clean_raw_dataset(raw)
    CLEANED_DATASET_FILE.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(CLEANED_DATASET_FILE, index=False)

    featured = build_feature_dataset(cleaned, include_content=include_content)
    FEATURED_DATASET_FILE.parent.mkdir(parents=True, exist_ok=True)
    featured.to_csv(FEATURED_DATASET_FILE, index=False)
    return featured


def select_features(featured: pd.DataFrame) -> FeatureSelectionResult:
    result = rank_features(featured)
    save_feature_selection(result)
    plot_feature_importance(result)

    base_columns = ["label"]
    if "url" in featured.columns:
        base_columns = ["url", "label"]
    selected = featured[base_columns + result.selected_features].copy()
    selected.to_csv(SELECTED_FEATURES_DATASET_FILE, index=False)
    return result


def run_training_pipeline(include_content: bool = True, raw_dataset_path: Path | None = None) -> TrainingResult:
    featured = prepare_datasets(include_content=include_content, raw_dataset_path=raw_dataset_path)
    select_features(featured)
    selected_dataset = pd.read_csv(SELECTED_FEATURES_DATASET_FILE)
    training_result = train_models(selected_dataset)
    save_model_comparison_csv(training_result.comparison)
    plot_model_comparison(training_result.comparison)
    write_evaluation_report(training_result.comparison, training_result.model_name, training_result.metrics)
    return training_result


def refresh_feature_ranking(featured_dataset_path: Path = FEATURED_DATASET_FILE) -> FeatureSelectionResult:
    featured = pd.read_csv(featured_dataset_path)
    result = rank_features(featured)
    save_feature_selection(result)
    plot_feature_importance(result)
    return result
