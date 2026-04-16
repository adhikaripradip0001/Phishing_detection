from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

from src.config import SCALER_FILE
from src.utils import save_joblib_artifact


@dataclass
class TabularPreprocessor:
    feature_names: list[str] = field(default_factory=list)
    imputer: SimpleImputer | None = None
    scaler: StandardScaler | None = None

    def fit(self, frame: pd.DataFrame) -> "TabularPreprocessor":
        working = self._prepare_frame(frame)
        self.feature_names = list(working.columns)
        self.imputer = SimpleImputer(strategy="median")
        self.scaler = StandardScaler()
        imputed = self.imputer.fit_transform(working)
        self.scaler.fit(imputed)
        return self

    def transform(self, frame: pd.DataFrame) -> np.ndarray:
        if self.imputer is None or self.scaler is None:
            raise RuntimeError("Preprocessor has not been fitted.")
        working = self._prepare_frame(frame)
        for column in self.feature_names:
            if column not in working.columns:
                working[column] = 0
        working = working[self.feature_names]
        imputed = self.imputer.transform(working)
        return self.scaler.transform(imputed)

    def fit_transform(self, frame: pd.DataFrame) -> np.ndarray:
        return self.fit(frame).transform(frame)

    def save(self, path: Path = SCALER_FILE) -> None:
        save_joblib_artifact(self, path)

    @staticmethod
    def load(path: Path = SCALER_FILE) -> "TabularPreprocessor":
        return joblib.load(path)

    @staticmethod
    def _prepare_frame(frame: pd.DataFrame) -> pd.DataFrame:
        working = frame.copy()
        for column in working.columns:
            working[column] = pd.to_numeric(working[column], errors="coerce")
        return working.replace([np.inf, -np.inf], np.nan)


def prepare_training_features(frame: pd.DataFrame, target_column: str = "label") -> tuple[pd.DataFrame, pd.Series]:
    features = frame.drop(columns=[target_column], errors="ignore").copy()
    if "url" in features.columns:
        features = features.drop(columns=["url"])
    target = frame[target_column].astype(int)
    return features, target
