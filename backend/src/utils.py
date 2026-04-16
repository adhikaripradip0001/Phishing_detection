from __future__ import annotations

import json
import logging
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

import joblib

from src.config import LOGS_DIR


def ensure_parent_dir(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def ensure_project_dirs(*paths: Path) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def setup_logger(name: str, log_file: Path, level: int = logging.INFO) -> logging.Logger:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger


def save_joblib_artifact(obj: Any, path: Path) -> None:
    ensure_parent_dir(path)
    joblib.dump(obj, path)


def load_joblib_artifact(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        return default
    return joblib.load(path)


def write_text_file(path: Path, content: str) -> None:
    ensure_parent_dir(path)
    path.write_text(content, encoding="utf-8")


def write_json_file(path: Path, payload: Any) -> None:
    ensure_parent_dir(path)
    if is_dataclass(payload):
        payload = asdict(payload)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def safe_numeric(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default
