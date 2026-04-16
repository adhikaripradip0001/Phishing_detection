import pandas as pd

from src.preprocessing import TabularPreprocessor


def test_preprocessing_fills_missing_values() -> None:
    frame = pd.DataFrame({"a": [1, None, 3], "b": [0, 1, None]})
    preprocessor = TabularPreprocessor().fit(frame)
    transformed = preprocessor.transform(frame)
    assert transformed.shape == (3, 2)
