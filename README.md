# 🧑‍💼 HR Attrition Analysis

Predicts which employees are likely to leave using XGBoost (AUC: 0.79) on real IBM HR data. Features Survival Analysis, Cost of Attrition calculator, Department × Role heatmap, Promotion Gap analysis, Manager Impact analysis, and an interactive prediction system.

## 🔍 What Makes This Unique
- **Survival Analysis** — Kaplan-Meier curves answer *when* employees leave, not just *if*. Log-rank test confirms statistical significance
- **Cost of Attrition Calculator** — estimates replacement cost per employee (150% of annual salary) broken down by department
- **Department × Role Heatmap** — identifies highest flight-risk combinations at a glance
- **Promotion Gap Analysis** — proves stagnation drives attrition with data
- **Manager Impact Analysis** — data proves "people leave managers, not companies"
- **SHAP Force Plot** — explains why each individual employee is at risk
- **Interactive Prediction** — single employee / batch / examples with per-employee cost impact

## 📊 Dataset
IBM HR Analytics — 1,470 employees × 35 features | Attrition rate ~16%

## 🛠️ Tech Stack
Python · XGBoost · Scikit-learn · SHAP · Lifelines · Imbalanced-learn · Power BI

## 📁 Project Structure
| File | Description |
|------|-------------|
| `HR_Attrition_Analysis_v4.ipynb` | Full notebook |
| `requirements.txt` | Dependencies |

## 🔍 Key Sections
| # | Section | What it does |
|---|---------|-------------|
| 1 | Libraries | All imports including lifelines |
| 2 | Load Dataset | Real IBM HR CSV from Kaggle |
| 3 | EDA | 6 charts — attrition by dept, income, overtime |
| 4 | Department Heatmap | Department × Job Role attrition rates |
| 5 | Survival Analysis | Kaplan-Meier + Log-rank test |
| 6 | Promotion Gap | Years since promotion vs attrition |
| 7 | Manager Impact | Years with manager vs attrition |
| 8 | Feature Engineering | 7 engineered features + RiskScore |
| 9 | SMOTE | Class imbalance handling |
| 10 | Model Comparison | LR, RF, Gradient Boosting, XGBoost |
| 11 | ROC Curve | All models compared |
| 12 | Hyperparameter Tuning | RandomizedSearchCV + Threshold optimization |
| 13 | SHAP | Feature importance + beeswarm + force plot |
| 14 | KMeans | 4 employee segments via PCA |
| 15 | Cost Calculator | Replacement cost by department + job level |
| 16 | Prediction System | Interactive menu — single / batch / examples |

## 📈 Results
| Model | AUC |
|-------|-----|
| Logistic Regression | ~0.72 |
| Random Forest | ~0.75 |
| Gradient Boosting | ~0.77 |
| XGBoost (tuned) | **0.79** |

## 🔑 Key Insights
- OverTime employees have significantly lower survival probability (Log-rank p=0.000)
- Employees with no promotion in 4+ years have highest attrition rate
- New manager relationships (0-1 year) spike attrition
- Low job satisfaction + poor work-life balance = strongest combined risk signal
- Top SHAP drivers: OverTime · MonthlyIncome · JobSatisfaction · YearsAtCompany

## 💰 Cost of Attrition
- Replacement cost estimated at 150% of annual salary (industry standard)
- Sales department carries highest replacement cost burden
- Retaining 30% of at-risk employees saves significant annual replacement spend

## 🧬 Survival Analysis Findings
- OverTime employees leave significantly earlier than non-overtime employees
- Frequent business travel group shows steeper survival curve decline
- Log-rank test p-value = 0.0000 — difference is not due to chance

## 📦 Dependencies
```bash
pip install -r requirements.txt
```

```
pandas
numpy
scikit-learn
imbalanced-learn
xgboost
shap
matplotlib
seaborn
lifelines
joblib
```

## 👤 Author
**KAVIN VENKAT**
[LinkedIn](www.linkedin.com/in/kavin-venkat-1710s0202) 
