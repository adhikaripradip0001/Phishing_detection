from __future__ import annotations

import os
from functools import lru_cache

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.config import API_DEFAULT_INCLUDE_CONTENT, FLASK_DEBUG, FLASK_HOST, FLASK_PORT
from src.predict import predict_single_url


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": os.getenv("API_CORS_ORIGIN", "*")}})

    @app.get("/health")
    def health() -> tuple[dict[str, str], int]:
        return {"status": "ok"}, 200

    @app.post("/api/predict")
    def predict() -> tuple[dict[str, object], int]:
        payload = request.get_json(silent=True) or {}
        url = str(payload.get("url", "")).strip()
        include_content = bool(payload.get("include_content", API_DEFAULT_INCLUDE_CONTENT))

        if not url:
            return {"error": "A URL is required."}, 400

        result = predict_single_url(url, include_content=include_content)
        status_code = 200 if result.get("success", False) else 400
        return result, status_code

    return app


@lru_cache(maxsize=1)
def get_app() -> Flask:
    return create_app()


if __name__ == "__main__":
    get_app().run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
