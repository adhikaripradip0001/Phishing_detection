# Methodology

## Introduction
This section presents the methodological framework adopted for the development and evaluation of an AI-based phishing website detection system. The research is grounded in a supervised machine learning paradigm in which website URLs are classified into two categories: phishing and legitimate. To improve detection reliability across diverse attack patterns, the framework employs a hybrid feature strategy that integrates URL lexical characteristics, domain-level intelligence derived from WHOIS records, and optional webpage content indicators obtained through live analysis.

The methodology is designed to satisfy three core requirements: reproducibility of experimentation, transparency of model evaluation, and practical feasibility of deployment. Accordingly, the study follows a structured pipeline comprising dataset construction, data cleaning and preprocessing, feature engineering, feature selection, comparative model training, and API-driven inference. This end-to-end structure supports academic rigor while also enabling real-time operational use through a web-based interface.

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

### 6.1 Module Setup and Dependencies
The training pipeline relies on the following core Python modules:

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
```

Key dependencies:
- pandas: Data manipulation and CSV handling
- scikit-learn: ML models, metrics, preprocessing
- numpy: Numerical computations
- joblib: Model serialization and artifact storage

### 6.2 Training Execution and Commands
Training is initiated via the backend main script from the project root:

```powershell
cd backend
python main.py train
```

This command orchestrates the full training pipeline:
1. Load raw dataset CSV files from `backend/data/raw/`
2. Apply data cleaning and feature extraction
3. Select informative features via ranking
4. Split data (80% train, 20% test, random seed 42)
5. Train candidate models with hyperparameter grid search
6. Evaluate and compare performance
7. Save best model and artifacts to `backend/models/`
8. Generate comparison report to `backend/reports/model_comparison.csv`

### 6.3 Training Configuration
The training process uses the following fixed parameters for reproducibility:

- **Train/Test Split**: 80% training, 20% held-out test
- **Random Seed**: 42 (fixed for reproducibility)
- **Cross-Validation Folds**: 3-fold for hyperparameter search
- **Feature Selection**: Top features selected by importance ranking

### 6.4 Hyperparameter Search Spaces
Grid search is applied over the following parameter ranges:

**Decision Tree**:
```python
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [5, 10, 20, None],
    'min_samples_split': [2, 5, 10]
}
```

**Random Forest**:
```python
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}
```

**Support Vector Machine (SVM)**:
```python
param_grid = {
    'C': [0.1, 1.0, 5.0, 10.0],
    'kernel': ['linear', 'rbf'],
    'gamma': ['scale', 'auto']
}
```

### 6.5 Training Pipeline Code Example
The core training workflow follows this pattern:

```python
from src.pipeline import PhishingPipeline

# Initialize pipeline
pipeline = PhishingPipeline()

# Load and prepare data
X_train, X_test, y_train, y_test = pipeline.load_and_split_data()

# Feature engineering and selection
X_train_features = pipeline.extract_features(X_train)
X_test_features = pipeline.extract_features(X_test)
selected_features = pipeline.select_top_features(X_train_features, y_train)

# Apply preprocessing
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_features[selected_features])
X_test_scaled = scaler.transform(X_test_features[selected_features])

# Train candidate models
models = {
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42),
    'SVM': SVC(random_state=42, probability=True)
}

best_model = None
best_score = 0

for name, model in models.items():
    # Grid search with cross-validation
    grid_search = GridSearchCV(model, param_grid, cv=3, scoring='f1')
    grid_search.fit(X_train_scaled, y_train)
    
    # Evaluate on test set
    y_pred = grid_search.predict(X_test_scaled)
    score = f1_score(y_test, y_pred)
    
    if score > best_score:
        best_score = score
        best_model = grid_search.best_estimator_

# Save artifacts
joblib.dump(best_model, 'backend/models/best_model.pkl')
joblib.dump(scaler, 'backend/models/preprocessor.pkl')
```

### 6.6 Model Training Output and Artifacts
After training completes, the following artifacts are generated:

- `backend/models/best_model.pkl`: Serialized best-performing classifier
- `backend/models/preprocessor.pkl`: Fitted StandardScaler for feature normalization
- `backend/models/selected_features.pkl`: List of selected feature names
- `backend/reports/model_comparison.csv`: Performance metrics for all candidate models

### 6.7 Candidate Models
The system trains and compares three supervised classifiers:
- Decision Tree
- Random Forest
- Support Vector Machine

A fixed random seed and train/test split are used for reproducibility, with hyperparameter search over predefined ranges as detailed in section 6.4.

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
