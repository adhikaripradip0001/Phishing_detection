from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BASE_DIR.parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
LOGS_DIR = BASE_DIR / "logs"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

PHISHING_URLS_FILE = RAW_DATA_DIR / "phishing_urls.csv"
LEGITIMATE_URLS_FILE = RAW_DATA_DIR / "legitimate_urls.csv"
COMBINED_RAW_FILE = RAW_DATA_DIR / "combined_raw.csv"

CLEANED_DATASET_FILE = PROCESSED_DATA_DIR / "cleaned_dataset.csv"
FEATURED_DATASET_FILE = PROCESSED_DATA_DIR / "featured_dataset.csv"
SELECTED_FEATURES_DATASET_FILE = PROCESSED_DATA_DIR / "selected_features_dataset.csv"
HOLDOUT_FEATURES_DATASET_FILE = PROCESSED_DATA_DIR / "holdout_features_dataset.csv"
FEATURE_RANKINGS_FILE = PROCESSED_DATA_DIR / "feature_rankings.csv"

BEST_MODEL_FILE = MODELS_DIR / "best_model.pkl"
SCALER_FILE = MODELS_DIR / "scaler.pkl"
LABEL_ENCODER_FILE = MODELS_DIR / "label_encoder.pkl"
SELECTED_FEATURES_FILE = MODELS_DIR / "selected_features.pkl"

CONFUSION_MATRIX_FILE = FIGURES_DIR / "confusion_matrix.png"
FEATURE_IMPORTANCE_FILE = FIGURES_DIR / "feature_importance.png"
MODEL_COMPARISON_FILE = FIGURES_DIR / "model_comparison.png"
ROC_CURVE_FILE = FIGURES_DIR / "roc_curve.png"
EVALUATION_REPORT_FILE = REPORTS_DIR / "evaluation_report.txt"
MODEL_COMPARISON_CSV_FILE = REPORTS_DIR / "model_comparison.csv"
TRAINING_LOG_FILE = LOGS_DIR / "training.log"
WHOIS_FAILURE_LOG_FILE = LOGS_DIR / "whois_failures.log"
SCRAPING_FAILURE_LOG_FILE = LOGS_DIR / "scraping_failures.log"

RANDOM_STATE = 42
TEST_SIZE = 0.2
VALIDATION_CV = 3

# Features excluded from training because they can encode source-collection bias
# and produce artificially perfect evaluation scores.
EXCLUDED_FEATURES = {
    "uses_https",
    "has_http_token",
}

API_DEFAULT_INCLUDE_CONTENT = True
CONTENT_REQUEST_TIMEOUT = 8

SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "secure",
    "update",
    "bank",
    "account",
    "confirm",
    "password",
    "signin",
    "authenticate",
    "authentication",
    "security",
    "support",
    "suspended",
    "urgent",
    "immediate",
    "reset",
    "unlock",
    "otp",
    "verification",
    "billing",
    "reward",
    "wallet",
    "invoice",
    "free",
    "prize",
    "winner",
    "claim",
    "limited",
    "expire",
    "expired",
    "bonus",
    "gift",
    "lottery",
    "offer",
    "cash",
]

COMMON_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "rebrand.ly",
}

PROTECTED_BRANDS = {
    "facebook",
    "instagram",
    "whatsapp",
    "google",
    "gmail",
    "paypal",
    "apple",
    "microsoft",
    "amazon",
    "netflix",
    "linkedin",
    "twitter",
    "xfinity",
    "outlook",
    "yahoo",
    "paytm",
    "phonepe",
    "gpay",
    "googlepay",
    "bhim",
    "sbi",
    "onlinesbi",
    "yono",
    "hdfc",
    "icici",
    "axis",
    "kotak",
    "pnb",
    "canara",
    "yesbank",
    "baroda",
    "bob",
    "unionbank",
    "indusind",
    "idfc",
    "aubank",
}

FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True

MODEL_SEARCH_SPACE = {
    "decision_tree": {
        "model__criterion": ["gini", "entropy", "log_loss"],
        "model__max_depth": [None, 5, 10, 20],
        "model__min_samples_split": [2, 5, 10],
    },
    "random_forest": {
        "model__n_estimators": [100, 200],
        "model__max_depth": [None, 10, 20],
        "model__min_samples_split": [2, 5, 10],
    },
    "svm": {
        "model__C": [0.1, 1.0, 5.0, 10.0],
        "model__kernel": ["linear", "rbf"],
        "model__gamma": ["scale", "auto"],
    },
}
