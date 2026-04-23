# Methodology

## 1. Research Design
This project uses a quantitative, experimental machine learning methodology for binary classification of websites into phishing (1) and legitimate (0). The system follows a hybrid detection strategy combining URL lexical signals, domain intelligence (WHOIS), and live page-content signals.

## 2. Data Acquisition and Dataset Construction
Data is collected from phishing and legitimate URL CSV sources and merged into a unified supervised dataset.

Steps:
- Load phishing and legitimate records from source CSVs.
- Normalize schema differences (column names and label conventions).
- Assign binary labels consistently.
- Merge into one dataset for training and evaluation.

## 3. Data Cleaning and Preprocessing
Preprocessing is applied before feature extraction to reduce noise and improve model reliability.

Steps:
- Normalize URL text and remove invalid records.
- Remove duplicates and empty values.
- Enforce label consistency and numeric typing.
- Handle missing values with safe defaults.

## 4. Hybrid Feature Engineering
The project extracts three feature families:

### 4.1 URL-Based Features
Examples include:
- URL length, domain length, path length
- Number of dots, hyphens, slashes, digits, special characters
- HTTPS usage, IP-address usage, query-string presence
- Suspicious keyword counts
- Brand-typosquatting similarity indicators

### 4.2 Domain-Based Features
Examples include:
- WHOIS availability
- Registrar availability
- Domain age
- Expiry horizon
- Registration duration

### 4.3 Content-Based Features (Live Scraping)
Examples include:
- Number of forms and input fields
- Password-field presence
- Internal/external links
- iframe and JavaScript redirect indicators
- Suspicious form-action patterns

If live scraping or WHOIS lookup fails, the system logs the event and falls back to available feature groups.

## 5. Feature Selection
After feature generation, features are ranked by predictive importance and top features are selected.

Goals:
- Reduce dimensionality
- Improve generalization
- Lower overfitting risk
- Maintain inference efficiency

The selected feature list is saved and reused during live prediction.

## 6. Model Development
The system trains multiple supervised classifiers and compares their performance.

Candidate models:
- Decision Tree
- Random Forest
- Support Vector Machine

A fixed random seed and train/test split are used for reproducibility, with hyperparameter search over predefined ranges.

## 7. Evaluation Protocol
Model performance is assessed using standard binary classification metrics:
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC (where applicable)

Additional outputs include:
- Confusion matrix
- Model comparison table
- Evaluation report and plots

### 7.1 Model Evaluation Table

The following table is generated from `backend/reports/model_comparison.csv`.

| Model | CV F1 | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| DecisionTreeClassifier | N/A | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

## 8. Inference Method (Live Prediction)
For each submitted URL:
1. Validate input.
2. Extract URL, domain, and optional content features.
3. Align feature row with saved selected-feature schema.
4. Apply saved preprocessing transform.
5. Predict class and phishing probability.
6. Apply risk heuristics for known high-risk patterns (for example, typo-brand signals).
7. Return label, confidence, probability, and key features to the frontend.

## 9. System Implementation
The methodology is implemented in a two-tier application architecture:
- Backend: Flask API + ML pipeline
- Frontend: React UI for URL submission and result visualization

This enables both research reproducibility and interactive demonstration.

## 10. Validation and Quality Assurance
Quality assurance includes:
- Unit tests for feature extraction and prediction flow
- Build verification for frontend stability
- Structured failure logging for WHOIS/scraping operations
- Artifact checks before prediction

## 11. Limitations and Practical Considerations
- Live scraping may fail due to SSL issues, bot blocking, or timeout.
- WHOIS availability varies by registrar/TLD.
- The system is decision support and should be combined with operational security controls.

## 12. Summary
This methodology provides an end-to-end, reproducible hybrid ML framework for phishing website detection, integrating data preparation, feature engineering, model training, evaluation, and live deployment in a unified pipeline.
