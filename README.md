# AI-Based Phishing Website Detection System Using Machine Learning

This project is a dissertation-aligned phishing website detection system built with supervised machine learning, hybrid feature engineering, a Flask prediction API, and a React user interface.

It follows a quantitative and experimental research design for binary classification of websites as `phishing` or `legitimate`, using URL-based, domain-based, and content-based features.

## Project Overview

The system implements a reproducible machine learning pipeline that:

1. Loads phishing and legitimate URLs from CSV sources.
2. Cleans and merges the raw data into a unified dataset.
3. Extracts hybrid features from the URL, domain WHOIS metadata, and page content.
4. Performs preprocessing, feature selection, and model comparison.
5. Trains multiple supervised classifiers and evaluates them with standard metrics.
6. Serves predictions through a Flask API and a React frontend.

## Dissertation Alignment

The implementation aligns with dissertation Chapters 1 to 3 by covering:

- Problem context and cybersecurity motivation.
- Quantitative experimental methodology.
- Supervised binary classification.
- Hybrid feature engineering.
- Model comparison and evaluation.
- Reproducibility through saved artifacts and CLI-driven execution.

## Feature Categories

### URL-Based Features

Examples include URL length, domain length, path length, number of dots, hyphens, slashes, digits, special characters, IP address presence, subdomain count, HTTPS usage, suspicious keyword counts, and query-string checks.

### Domain-Based Features

Examples include domain age, expiry days, registration length, WHOIS availability, registrar availability, and date-existence flags.

### Content-Based Features

Examples include number of forms, input fields, password fields, internal/external links, iframe presence, JavaScript redirects, scripts, title and favicon existence, suspicious form actions, empty form actions, and mailto usage.

## Dataset Sources

This codebase is structured to support CSV datasets from sources such as:

- PhishTank or OpenPhish for phishing URLs.
- Tranco or similar trusted lists for legitimate URLs.
- Optional benchmark datasets from UCI or Kaggle.

For convenience, the repository includes small sample CSVs under `backend/data/raw/` so the pipeline can be exercised immediately.

### Supported CSV Schemas (Auto-Mapped)

You can use common public dataset column names without manual renaming.

- URL columns supported: `url`, `URL`, `link`, `website`, `domain`
- Label columns supported: `label`, `class`, `target`, `result`, `status`

Label values are normalized automatically to binary classes:

- Phishing-like values map to `1`: `1`, `phishing`, `phish`, `malicious`, `bad`, `fraud`, `yes`, `true`
- Legitimate-like values map to `0`: `0`, `-1`, `legitimate`, `legit`, `benign`, `good`, `safe`, `no`, `false`

If label columns are missing in split source files, labels are assigned by filename:

- `phishing_urls.csv` -> `1`
- `legitimate_urls.csv` -> `0`

## Folder Structure

The project is organized as follows:

- `backend/` for the machine learning pipeline and Flask API.
- `frontend/` for the React user interface.
- `backend/data/raw/` for source CSVs.
- `backend/data/processed/` for cleaned, featured, and selected datasets.
- `backend/models/` for trained artifacts.
- `backend/reports/` for metrics, plots, and evaluation output.
- `backend/logs/` for WHOIS and scraping failures.
- `backend/notebooks/` for exploratory and dissertation-oriented notebook work.

## Backend Installation

From the `backend/` directory:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Frontend Installation

From the `frontend/` directory:

```bash
npm install
```

If you want the frontend to point to a non-default API URL, create a `.env` file:

```bash
VITE_API_BASE_URL=http://localhost:5000
```

## How to Train

Run from the `backend/` directory:

```bash
python main.py train
```

To train from any custom combined CSV path (with auto schema mapping):

```bash
python main.py train --dataset "D:/path/to/your_dataset.csv" --no-content
```

This will:

- load the raw CSV sources,
- clean and merge the data,
- extract features,
- rank features,
- train and compare the models,
- save the best model and preprocessing artifact,
- generate evaluation outputs.

## How to Evaluate

Run:

```bash
python main.py evaluate
```

To evaluate using a custom combined dataset path:

```bash
python main.py evaluate --dataset "D:/path/to/your_dataset.csv" --no-content
```

This regenerates the datasets, retrains the candidates, and outputs the comparison table and evaluation report.

## How to Run the Flask API

Run:

```bash
python main.py run-api
```

The API exposes:

- `GET /health`
- `POST /api/predict`

### Prediction Request Example

```json
{
  "url": "https://example.com",
  "include_content": true
}
```

### Prediction Response Example

```json
{
  "success": true,
  "predicted_label": "legitimate",
  "phishing_probability": 0.03,
  "confidence": 0.97
}
```

## How to Run the React Frontend

From the `frontend/` directory:

```bash
npm run dev
```

Open the local Vite URL shown in the terminal, then enter a website URL to classify it.

## CLI Commands

The backend supports the following commands:

```bash
python main.py train
python main.py evaluate
python main.py train --dataset "D:/path/to/your_dataset.csv" --no-content
python main.py evaluate --dataset "D:/path/to/your_dataset.csv" --no-content
python main.py predict --url "https://example.com"
python main.py run-api
```

## Generated Outputs

The training pipeline produces:

- `backend/models/best_model.pkl`
- `backend/models/scaler.pkl`
- `backend/models/label_encoder.pkl`
- `backend/models/selected_features.pkl`
- `backend/reports/evaluation_report.txt`
- `backend/reports/figures/confusion_matrix.png`
- `backend/reports/figures/feature_importance.png`
- `backend/reports/figures/model_comparison.png`
- `backend/reports/figures/roc_curve.png`
- `backend/data/processed/feature_rankings.csv`
- `backend/data/processed/cleaned_dataset.csv`
- `backend/data/processed/featured_dataset.csv`
- `backend/data/processed/selected_features_dataset.csv`

## Example Screenshots

Placeholder section for dissertation documentation screenshots of:

- model training output,
- Flask API response,
- React frontend prediction screen,
- evaluation plots.

## Future Improvements

- Expand the labeled dataset with larger public corpora.
- Add model calibration and threshold tuning.
- Introduce SHAP-based explainability for dissertation defense.
- Containerize the backend and frontend for deployment.
- Add authentication and rate limiting to the API.
