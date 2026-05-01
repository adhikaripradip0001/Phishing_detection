# AI-Based Phishing Website Detection System

## 1. Project Overview
This project is a full-stack phishing website detection platform built with supervised machine learning. It classifies URLs into two classes:
- phishing
- legitimate

The system combines hybrid feature engineering and live prediction:
- URL lexical features
- domain/WHOIS features
- optional live content scraping features

The project includes:
- a backend ML pipeline and Flask API
- a frontend React interface
- saved model artifacts and reports
- tests for key detection components

## 2. Objectives
- Detect phishing websites accurately in real time.
- Use multiple feature families to improve robustness.
- Support reproducible training and evaluation.
- Provide a user-friendly interface for classification.
- Generate dissertation-ready outputs (reports and comparisons).

## 3. Technology Stack
### Backend
- Python 3
- Flask
- scikit-learn
- pandas, numpy
- beautifulsoup4, requests
- python-whois, tldextract

### Frontend
- React
- Vite
- Axios

### Testing
- pytest

## 4. Repository Structure
- backend/: ML pipeline, API, data, models, reports, tests
- frontend/: React UI and API client
- start-dev.ps1: one-command local startup script
- README.md: quick project guide
- PROJECT_DOCUMENTATION.md: this full documentation

## 5. System Architecture
The platform follows a layered architecture.

### 5.1 Presentation Layer
- React frontend accepts URL input and displays prediction results.

### 5.2 API Layer
- Flask API exposes:
- GET /health
- POST /api/predict

### 5.3 Intelligence Layer
- Feature extraction engine computes URL, domain, and content features.
- Preprocessor transforms features to model-ready format.
- Best trained model predicts phishing probability.
- Risk heuristics handle high-risk patterns (for example typo-brand domains).

### 5.4 Data and Artifact Layer
- Raw and processed datasets in backend/data.
- Trained artifacts in backend/models.
- Evaluation outputs in backend/reports.
- Operational logs in backend/logs.

## 6. End-to-End Workflow
### 6.1 Offline Training Workflow
1. Load phishing and legitimate URL data.
2. Clean and normalize records.
3. Build hybrid feature dataset.
4. Rank/select informative features.
5. Train candidate models.
6. Compare performance and choose best model.
7. Save model, preprocessor, and selected features.
8. Generate reports and figures.

### 6.2 Online Prediction Workflow
1. User submits URL from frontend.
2. Frontend sends request to Flask API.
3. Backend validates input.
4. Backend extracts URL/domain/content features.
5. Features are aligned with selected schema.
6. Preprocessor transforms feature row.
7. Model predicts class and probability.
8. API returns label, confidence, and key feature summary.

## 9. API Documentation
### 9.1 Health Check
- Method: GET
- Endpoint: /health
- Response example:

```json
{
  "status": "ok"
}
```

### 9.2 URL Prediction
- Method: POST
- Endpoint: /api/predict
- Request example:

```json
{
  "url": "https://example.com",
  "include_content": true
}
```

- Response example:

```json
{
  "success": true,
  "predicted_label": "legitimate",
  "phishing_probability": 0.03,
  "confidence": 0.97
}
```

## 10. Setup and Execution
### 10.1 Backend Setup
From project root:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r backend\requirements.txt
```

### 10.2 Frontend Setup

```powershell
cd frontend
npm install
```

### 10.3 Train Model

```powershell
cd backend
python main.py train
```

### 10.4 Run API

```powershell
cd backend
python main.py run-api
```

### 10.5 Run Frontend

```powershell
cd frontend
npm run dev
```

### 10.6 One-Command Startup
From project root:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-dev.ps1
```

## 11. Testing
Run backend tests:

```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest
```

Focused tests used during development:

```powershell
..\.venv\Scripts\python.exe -m pytest tests\test_url_features.py tests\test_prediction.py
```

## 12. Logging and Monitoring
- WHOIS lookup failures are logged.
- Content scraping failures are logged.
- Evaluation reports and figures are generated under backend/reports.

## 13. Known Limitations
- Live scraping can fail due to SSL issues, bot protections, or timeout.
- WHOIS data may be unavailable for certain domains.
- Small or homogeneous datasets can inflate reported metrics.
- The classifier should be used as decision support, not sole authority.

## 14. Security and Operational Considerations
- Validate and sanitize all incoming URL inputs.
- Keep dependency versions updated.
- Add API rate limiting for production deployment.
- Use a production WSGI server for deployment.
- Add model versioning and periodic retraining schedule.

## 15. Ethical Considerations
- Use this system as decision support, not as a sole automated authority for blocking or legal action.
- Minimize false positives to avoid unfairly flagging legitimate businesses and websites.
- Minimize false negatives to reduce exposure of users to harmful phishing pages.
- Respect data privacy: do not collect personal user data beyond what is needed for URL-based analysis.
- Limit retention of logs and ensure any stored data is protected and access-controlled.
- Be transparent about model confidence, uncertainty, and system limitations.
- Regularly audit model behavior for bias caused by dataset imbalance or narrow domain coverage.
- Ensure responsible scraping practices: obey legal constraints, terms of service, and rate limits.
- Maintain human oversight for high-impact decisions in operational deployments.

## 16. Suggested Future Enhancements
- Expand data coverage using additional public sources.
- Add model calibration and threshold tuning.
- Add SHAP-based explainability.
- Add Dockerized deployment.
- Add authentication and audit trail for enterprise use.

## 17. Authoring Notes
This documentation complements:
- README.md for quick usage
- backend/reports/methodology.md for research methodology details
