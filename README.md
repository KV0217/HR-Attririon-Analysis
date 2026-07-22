# HR Attrition Analysis & Cost Prediction

## Overview
Machine Learning pipeline predicting which employees are likely to leave using XGBoost (AUC: 0.79) on real IBM HR data. 

*Note: The FastAPI deployment for this model is available in the [HR-ATTRITION-API](https://github.com/KV0217/HR-ATTRITION-API) repository.*

## Key Features
- **Predictive Modeling:** 83% accuracy using XGBoost.
- **Survival Analysis:** Kaplan-Meier survival analysis to identify 90-day at-risk windows (log-rank p < 0.0001).
- **Explainability:** SHAP values used to interpret feature importance.
- **Data Balancing:** Handled imbalanced HR records using SMOTE.
- **Cost of Attrition Calculator:** 150% salary replacement model connecting ML outputs to direct business ROI.

## Tech Stack
- **Machine Learning:** Python, XGBoost, Lifelines (Survival Analysis), SHAP, SMOTE
- **Data Storage:** SQLite
- **Visualization:** Power BI (Department heatmaps & interactive prediction system)

## Business Value
This project moves beyond just predicting attrition by actively calculating the financial cost of losing an employee, allowing HR departments to intervene precisely when it makes financial sense.
