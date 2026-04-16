from __future__ import annotations

import pandas as pd

from src.content_features import extract_content_features
from src.domain_features import extract_domain_features
from src.url_features import extract_url_features


def build_feature_row(url: str, include_content: bool = True) -> dict[str, float]:
    row = extract_url_features(url)
    row.update(extract_domain_features(url))
    row.update(extract_content_features(url, enable_fetch=include_content))
    return row


def build_feature_dataset(frame: pd.DataFrame, include_content: bool = True) -> pd.DataFrame:
    if frame.empty:
        return frame.copy()

    records = []
    for _, record in frame.iterrows():
        url = str(record["url"])
        features = build_feature_row(url, include_content=include_content)
        features["url"] = url
        features["label"] = int(record["label"])
        records.append(features)

    feature_frame = pd.DataFrame.from_records(records)
    ordered_columns = ["url", "label"] + [column for column in feature_frame.columns if column not in {"url", "label"}]
    return feature_frame[ordered_columns]
