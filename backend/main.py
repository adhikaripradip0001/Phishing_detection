from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from app.app import get_app
from src.config import FEATURED_DATASET_FILE
from src.evaluate import evaluate_saved_model
from src.pipeline import prepare_datasets, run_training_pipeline, select_features
from src.predict import predict_single_url
from src.train import train_models


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI-Based Phishing Website Detection System")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train_parser = subparsers.add_parser("train", help="Build datasets and train models")
    train_parser.add_argument("--no-content", action="store_true", help="Skip live content scraping")
    train_parser.add_argument("--dataset", type=str, help="Path to a custom combined CSV dataset")

    eval_parser = subparsers.add_parser("evaluate", help="Run evaluation on the featured dataset")
    eval_parser.add_argument("--no-content", action="store_true", help="Skip live content scraping")
    eval_parser.add_argument("--dataset", type=str, help="Path to a custom combined CSV dataset")

    predict_parser = subparsers.add_parser("predict", help="Predict a single URL")
    predict_parser.add_argument("--url", required=True, help="URL to classify")
    predict_parser.add_argument("--no-content", action="store_true", help="Skip live content scraping")

    subparsers.add_parser("run-api", help="Start the Flask API")
    return parser


def run_train(include_content: bool, dataset_path: str | None = None) -> None:
    custom_path = Path(dataset_path) if dataset_path else None
    result = run_training_pipeline(include_content=include_content, raw_dataset_path=custom_path)
    print(json.dumps({"best_model": result.model_name, "metrics": result.metrics}, indent=2))


def run_evaluate(include_content: bool, dataset_path: str | None = None) -> None:
    custom_path = Path(dataset_path) if dataset_path else None
    featured = prepare_datasets(include_content=include_content, raw_dataset_path=custom_path)
    select_features(featured)
    selected_dataset = pd.read_csv(FEATURED_DATASET_FILE.parent / "selected_features_dataset.csv")
    comparison, metrics, model_name = evaluate_saved_model(selected_dataset)
    print(comparison.to_string(index=False))
    print(json.dumps({"best_model": model_name, "metrics": metrics}, indent=2))


def run_predict(url: str, include_content: bool) -> None:
    print(json.dumps(predict_single_url(url, include_content=include_content), indent=2))


def run_api() -> None:
    app = get_app()
    app.run(host="0.0.0.0", port=5000, debug=True)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    include_content = not getattr(args, "no_content", False)

    if args.command == "train":
        run_train(include_content, getattr(args, "dataset", None))
    elif args.command == "evaluate":
        run_evaluate(include_content, getattr(args, "dataset", None))
    elif args.command == "predict":
        run_predict(args.url, include_content)
    elif args.command == "run-api":
        run_api()


if __name__ == "__main__":
    main()
