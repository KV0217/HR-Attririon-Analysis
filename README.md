# 🧑‍💼 HR Attrition Analysis

Predicts which employees are likely to leave using XGBoost(~0.79) on real IBM HR data. Features Kaplan-Meier Survival Analysis, Cost of Attrition calculator, Department × Role heatmap, Promotion Gap analysis, Manager Impact analysis, SQL Risk Analysis, and an interactive prediction system with per-employee cost impact.

## 🔍 What Makes This Unique
- **Survival Analysis** — Kaplan-Meier curves answer *when* employees leave, not just *if*. Log-rank test (p=0.0000) confirms OverTime employees leave significantly earlier
- **Cost of Attrition Calculator** — replacement cost per employee (150% of annual salary) broken down by department and job level
- **Department × Role Heatmap** — identifies highest flight-risk combinations visually
- **Promotion Gap Analysis** — proves stagnation drives attrition with data
- **Manager Impact Analysis** — data proves "people leave managers, not companies"
- **SQL Risk Analysis** — attrition risk ranking, cost analysis, overtime matrix using CTEs and Window Functions
- **SHAP Force Plot** — explains why each individual employee is flagged as at-risk
- **Threshold Optimization** — finds best classification threshold for maximum attrition recall

## 📊 Dataset
IBM HR Analytics — 1,470 employees × 35 features | Attrition rate: ~16%

## 🛠️ Tech Stack
Python · XGBoost · Scikit-learn · SHAP · Lifelines · Imbalanced-learn · SQLite · Power BI

## 📁 Project Structure
| File | Description |
|------|-------------|
| `hr-attrition.ipynb` | Full notebook |
| `requirements.txt` | Dependencies |

## 🔍 Key Sections
| # | Section | What it does |
|---|---------|-------------|
| 1 | Libraries | All imports including lifelines |
| 2 | Load Dataset | IBM HR CSV — 35 features |
| 3 | EDA | 6 charts — attrition by dept, income, overtime |
| 3b | SQL Risk Analysis | CTEs · Window Functions · Cost analysis |
| 4 | Department Heatmap | Department × Job Role attrition rates |
| 5 | Survival Analysis | Kaplan-Meier + Log-rank statistical test |
| 6 | Promotion Gap | Years since promotion vs attrition rate |
| 7 | Manager Impact | Years with manager vs attrition — proves "leave managers" |
| 8 | Feature Engineering | IncomePerYear · TenureRatio · RiskScore · PromotionGap |
| 9 | SMOTE | Class imbalance handling |
| 10 | Model Comparison | LR · RF · Gradient Boosting · XGBoost pipeline |
| 11 | ROC Curve | All models compared |
| 12 | Hyperparameter Tuning | RandomizedSearchCV + Threshold optimization |
| 13 | SHAP | Feature importance + beeswarm + force plot |
| 14 | KMeans | 4 employee risk segments via PCA |
| 15 | Cost Calculator | Replacement cost by department + job level |
| 16 | Prediction System | Interactive menu — single / batch / examples |

## 📈 Model Results
| Model | AUC |
|-------|-----|
| Logistic Regression | ~0.72 |
| Random Forest | ~0.75 |
| Gradient Boosting | ~0.77 |
| **XGBoost (Tuned)** | **~0.79** |

## 🗄️ SQL Highlights
```sql
-- Cost of Attrition by Department (CTE + Window Function)
WITH dept_cost AS (
    SELECT Department,
           ROUND(SUM(CASE WHEN Attrition=1
                 THEN MonthlyIncome*12 ELSE 0 END),0) AS salary_at_risk
    FROM hr GROUP BY Department
)
SELECT *, ROUND(salary_at_risk*1.5,0) AS replacement_cost,
    RANK() OVER (ORDER BY salary_at_risk DESC) AS cost_rank
FROM dept_cost ORDER BY replacement_cost DESC
```

## 🔑 Key Insights
- OverTime employees leave significantly earlier — Log-rank p=0.0000
- Employees with 5+ years no promotion have highest attrition rate
- New manager relationships (0-1 year) spike attrition dramatically
- Low JobSatisfaction + OverTime = strongest combined risk signal
- Top SHAP drivers: OverTime · MonthlyIncome · JobSatisfaction · YearsAtCompany

## 🧬 Survival Analysis Findings
- OverTime group has steeper survival curve decline from year 1
- Frequent travel group shows earlier departure pattern
- Statistical significance confirmed via log-rank test

## 💰 Cost of Attrition
- Replacement cost = 150% of annual salary (industry standard)
- Sales department carries highest total replacement cost burden
- Interactive calculator shows savings from retention interventions

## 👤 Author
**KAVIN VENKAT**
[LinkedIn](www.linkedin.com/in/kavin-venkat-1710s0202) 
