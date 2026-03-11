# 🧑‍💼 HR Attrition Analysis

Predicts which employees are likely to leave using XGBoost (AUC: 0.79)
on real IBM HR data. Features Survival Analysis, Cost of Attrition
calculator, Department heatmap, and interactive prediction system.

🔍 What Makes This Unique
- Survival Analysis           — Kaplan-Meier curves showing *when* employees leave
- Cost Calculator             — $X replacement cost identified (150% of annual salary)
- Department × Role Heatmap   — highest flight-risk combinations
- Promotion Gap Analysis      — stagnation drives attrition
- Manager Impact Analysis     — proves "people leave managers not companies"
- SHAP Force Plot             — explains *why* each employee is at risk

📊 Dataset
IBM HR Analytics — 1,470 employees × 35 features | Attrition rate ~16%

🛠️ Tech Stack
Python · XGBoost · Scikit-learn · SHAP · Lifelines · Imbalanced-learn · Power BI

 📁 Project Structure
           | File                             -       Description |
           | `HR_Attrition_Analysis_v4.ipynb` -       Full notebook |
           | `requirements.txt`               -       Dependencies |

🔍 Key Steps
1.  EDA                    —    Attrition by Department, Income, Age, OverTime
2.  Heatmap                —    Department × Job Role attrition rates
3.  Survival Analysis      —    Kaplan-Meier + Log-rank test
4.  Promotion Gap          —    Years since promotion vs attrition
5.  Manager Impact         —    Years with manager vs attrition
6.  SMOTE                  —    Class imbalance handling
7.  Models                 —    LR, RF, Gradient Boosting, XGBoost
8.  Tuning                 —    RandomizedSearchCV + Threshold optimization
9.  SHAP                   —    Feature importance + beeswarm + force plot
10. KMeans                 —    4 employee segments via PCA
11. Cost Calculator        —    Replacement cost by department
12. rediction System       —    Single / batch / examples

📈 Results

             Model      -     AUC 

| Logistic Regression     -   0.72 |
| Random Forest           -   0.75 |
| Gradient Boosting       -   0.77 |
| XGBoost (tuned)         -   0.79 |

💡 Top Attrition Drivers
- OverTime
- Monthly Income
- Job Satisfaction
- Years at Company
- Business Travel
- Years Since Last Promotion

👤 Author
KAVIN VENKAT V R 
[LinkedIn](YOUR_LINKEDIN_URL) · [GitHub](YOUR_GITHUB_URL)
