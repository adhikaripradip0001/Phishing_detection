from __future__ import annotations

import pandas as pd


def clean_raw_dataset(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.copy()
    cleaned["url"] = cleaned["url"].astype(str).str.strip()
    cleaned = cleaned.dropna(subset=["url"])
    cleaned = cleaned[cleaned["url"] != ""]
    cleaned = cleaned.drop_duplicates(subset=["url", "label"]).reset_index(drop=True)
    cleaned["label"] = cleaned["label"].fillna(0).astype(int)
    return cleaned
