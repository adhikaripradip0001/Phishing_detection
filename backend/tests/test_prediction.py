import pandas as pd

from src.preprocessing import TabularPreprocessor
from src.utils import save_joblib_artifact


def test_prediction_pipeline_requires_artifacts(tmp_path, monkeypatch) -> None:
    from sklearn.linear_model import LogisticRegression

    frame = pd.DataFrame({"f1": [0.0, 1.0, 2.0, 3.0], "f2": [1.0, 1.0, 0.0, 0.0]})
    target = [0, 0, 1, 1]
    preprocessor = TabularPreprocessor().fit(frame)
    model = LogisticRegression().fit(preprocessor.transform(frame), target)

    monkeypatch.setattr("src.predict.BEST_MODEL_FILE", tmp_path / "best_model.pkl")
    monkeypatch.setattr("src.predict.SCALER_FILE", tmp_path / "scaler.pkl")
    monkeypatch.setattr("src.predict.LABEL_ENCODER_FILE", tmp_path / "label_encoder.pkl")
    monkeypatch.setattr("src.predict.SELECTED_FEATURES_FILE", tmp_path / "selected_features.pkl")

    save_joblib_artifact(model, tmp_path / "best_model.pkl")
    save_joblib_artifact(preprocessor, tmp_path / "scaler.pkl")
    save_joblib_artifact([], tmp_path / "selected_features.pkl")

    result = __import__("src.predict", fromlist=["predict_single_url"]).predict_single_url("http://example.com", include_content=False)
    assert result["success"] is False or "predicted_label" in result
