from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from src.config import COMBINED_RAW_FILE, LEGITIMATE_URLS_FILE, PHISHING_URLS_FILE
from src.utils import ensure_parent_dir


URL_COLUMN_CANDIDATES = ["url", "URL", "link", "Link", "website", "Website", "domain", "Domain"]
LABEL_COLUMN_CANDIDATES = [
    "label",
    "Label",
    "class",
    "Class",
    "class_label",
    "CLASS_LABEL",
    "target",
    "Target",
    "result",
    "Result",
    "status",
    "Status",
]

PHISHING_LABEL_TOKENS = {"1", "phishing", "phish", "malicious", "bad", "fraud", "yes", "true"}
LEGITIMATE_LABEL_TOKENS = {"0", "legitimate", "legit", "benign", "good", "safe", "no", "false", "-1"}


def _first_existing_column(columns: Iterable[str], candidates: Iterable[str]) -> str | None:
    column_set = {column.strip().lower(): column for column in columns}
    for candidate in candidates:
        key = candidate.strip().lower()
        if key in column_set:
            return column_set[key]
    return None


def _normalize_label_value(value: object, fallback_label: int) -> int:
    if pd.isna(value):
        return fallback_label

    text = str(value).strip().lower()
    if text in PHISHING_LABEL_TOKENS:
        return 1
    if text in LEGITIMATE_LABEL_TOKENS:
        return 0

    try:
        numeric = float(text)
        if numeric > 0:
            return 1
        return 0
    except ValueError:
        return fallback_label


def _normalize_schema(frame: pd.DataFrame, default_label: int) -> pd.DataFrame:
    url_column = _first_existing_column(frame.columns, URL_COLUMN_CANDIDATES)
    label_column = _first_existing_column(frame.columns, LABEL_COLUMN_CANDIDATES)

    # Support pre-engineered datasets that already contain numeric features + class labels.
    if url_column is None and label_column is not None:
        normalized = frame.copy()
        normalized["label"] = normalized[label_column].apply(lambda value: _normalize_label_value(value, default_label))

        drop_candidates = [label_column]
        id_column = _first_existing_column(normalized.columns, ["id", "ID", "index", "Index"])
        if id_column:
            drop_candidates.append(id_column)

        feature_columns = [
            column
            for column in normalized.columns
            if column not in set(drop_candidates) and column.strip().lower() != "label"
        ]
        normalized = normalized[feature_columns + ["label"]]
        return normalized.reset_index(drop=True)

    if url_column is None:
        raise ValueError(
            "Could not find a URL column. Supported names include: "
            f"{', '.join(URL_COLUMN_CANDIDATES)}"
        )

    normalized = frame.copy()
    normalized["url"] = normalized[url_column].astype(str).str.strip()

    if label_column is None:
        normalized["label"] = default_label
    else:
        normalized["label"] = normalized[label_column].apply(lambda value: _normalize_label_value(value, default_label))

    normalized = normalized[["url", "label"]]
    normalized = normalized[normalized["url"] != ""]
    return normalized.reset_index(drop=True)


def _load_url_csv(path: Path, label: int) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["url", "label"])
    frame = pd.read_csv(path)
    frame = _normalize_schema(frame, default_label=label)
    frame["label"] = frame["label"].astype(int)
    return frame


def load_phishing_and_legitimate_data() -> pd.DataFrame:
    phishing = _load_url_csv(PHISHING_URLS_FILE, 1)
    legitimate = _load_url_csv(LEGITIMATE_URLS_FILE, 0)
    combined = pd.concat([phishing, legitimate], ignore_index=True)
    if combined.empty and COMBINED_RAW_FILE.exists():
        combined = pd.read_csv(COMBINED_RAW_FILE)
    return combined.drop_duplicates(subset=["url", "label"]).reset_index(drop=True)


def save_raw_dataset(frame: pd.DataFrame) -> Path:
    ensure_parent_dir(COMBINED_RAW_FILE)
    frame.to_csv(COMBINED_RAW_FILE, index=False)
    return COMBINED_RAW_FILE


def load_raw_dataset(path: Path | None = None) -> pd.DataFrame:
    dataset_path = path or COMBINED_RAW_FILE
    if not dataset_path.exists():
        return load_phishing_and_legitimate_data()
    frame = pd.read_csv(dataset_path)
    return _normalize_schema(frame, default_label=0)
