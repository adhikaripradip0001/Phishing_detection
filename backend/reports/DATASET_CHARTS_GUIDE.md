# Dataset Visualization Charts Guide

This document provides an overview of all available dataset visualization charts for your dissertation presentation.

## Available Charts

### 1. Dataset Class Balance Distribution
**File:** `dataset_class_balance.png`
**Description:** Pie chart showing the percentage distribution of phishing vs legitimate URLs in the cleaned dataset. Displays the proportion of each class in your training data.
**Best For:** Showing data balance and class representation in your dataset

---

### 2. Phishing vs Legitimate URLs - Record Count
**File:** `dataset_size_comparison.png`
**Description:** Bar chart comparing the absolute number of phishing and legitimate URL records. Shows raw counts for each class.
**Best For:** Demonstrating the scale of your dataset and class representation

---

### 3. Feature Reduction: All vs Selected
**File:** `feature_reduction_chart.png`
**Description:** Bar chart showing the reduction in feature count from all engineered features to the final selected features. Displays dimensionality reduction percentage.
**Best For:** Highlighting feature selection effectiveness and dimensionality reduction

---

### 4. Top Features Importance (New)
**File:** `feature_importance_top20.png`
**Description:** Horizontal bar chart showing the top 20 features ranked by Random Forest importance (or fallback importance). Useful for highlighting which engineered features contributed most to model predictions.
**Best For:** Explaining feature relevance and supporting model interpretability in results discussion

---

### 5. Top Features Importance — Normalized & Annotated (New)
**File:** `feature_importance_top20_annotated.png`
**Description:** Horizontal bar chart of the top 20 features with normalized importance (proportion of total importance) and annotated percentage labels. Use this in presentations to clearly communicate relative feature contributions.
**Best For:** Presentation slides and results discussion where clear percentage annotations improve readability

---

### 6. Feature Shape Overview (Project-Aligned)
**File:** `feature_shape_overview_project_aligned.png`
**Description:** 2x3 panel of KDE density plots covering lexical, domain, and content features. This is the best figure for showing distribution shapes across your full phishing detection pipeline.
**Best For:** Figure sections that need a balanced summary of feature shapes across feature families

---

### 4. Dataset Distribution Chart
**File:** `dataset_distribution_chart.svg`
**Description:** Visual representation of phishing vs legitimate dataset proportions.
**Best For:** Quick overview of class balance

---

### 5. Dataset Collection Flow
**File:** `dataset_collection_flow.svg`
**Description:** Flowchart showing how data flows through collection from multiple sources.
**Best For:** Explaining data acquisition methodology

---

### 6. Data Processing Pipeline
**File:** `data_processing_pipeline.svg`
**Description:** Diagram showing the data processing stages and transformations.
**Best For:** Explaining preprocessing and data cleaning steps

---

### 7. Corrected Experimental Pipeline
**File:** `corrected_experimental_pipeline.svg`
**Description:** Comprehensive pipeline diagram showing all stages from raw data to final model.
**Best For:** Providing complete overview of the experimental methodology

---

### 8. Model Comparison
**File:** `model_comparison.png` and `model_comparison_graph.svg`
**Description:** Bar charts comparing performance metrics across different ML models (Decision Tree, Random Forest, SVM).
**Best For:** Showing model selection process and comparative performance

---

### 9. Feature Importance
**File:** `feature_importance.png`
**Description:** Bar chart ranking features by their importance in the trained model.
**Best For:** Explaining which features are most predictive for phishing detection

---

### 10. ROC Curve
**File:** `roc_curve.png`
**Description:** ROC curve showing model performance across different classification thresholds.
**Best For:** Demonstrating model discrimination ability and AUC score

---

### 11. Confusion Matrix
**File:** `confusion_matrix.png`
**Description:** Heatmap showing True Positives, True Negatives, False Positives, and False Negatives.
**Best For:** Detailed analysis of prediction accuracy and error types

---

## Recommended Presentation Order

For a clear dissertation presentation, consider using the charts in this order:

1. **Dataset Collection Flow** - Explain where data comes from
2. **Dataset Class Balance** - Show your data composition
3. **Dataset Size Comparison** - Quantify your dataset
4. **Feature Reduction Chart** - Explain feature engineering effectiveness
5. **Data Processing Pipeline** - Show data cleaning and preparation
6. **Model Comparison** - Present candidate models and selection
7. **Feature Importance** - Show key predictive features
8. **Confusion Matrix** - Detail model accuracy
9. **ROC Curve** - Demonstrate model performance metrics

## Using These Charts in Your Document

All charts are located in: `backend/reports/figures/`

### Embedding in Markdown
```markdown
![Chart Title](backend/reports/figures/filename.png)
```

### Embedding in LaTeX
```latex
\includegraphics[width=0.8\textwidth]{backend/reports/figures/filename.png}
```

### Including in Presentations
You can directly reference these PNG/SVG files in:
- PowerPoint (Insert > Pictures)
- Google Slides (Insert > Image)
- Reveal.js presentations
- Web-based presentations

## Chart Specifications

- **Resolution:** 300 DPI (suitable for printing)
- **Format:** PNG (raster) and SVG (vector)
- **Color Scheme:** Professional blues, reds, and greens
- **Font:** Bold, readable at presentation sizes

---

*Generated for dissertation presentation purposes*
