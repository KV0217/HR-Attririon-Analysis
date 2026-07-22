import mlflow
import mlflow.xgboost
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import pandas as pd
import numpy as np

# Mock implementation demonstrating MLflow tracking for HR Attrition
def train_and_log_model():
    # 1. Setup MLflow Experiment
    mlflow.set_experiment("HR_Attrition_XGBoost")
    
    # Mock Data
    X = np.random.rand(100, 10)
    y = np.random.randint(2, size=100)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run():
        # 2. Define Hyperparameters
        params = {
            "objective": "binary:logistic",
            "max_depth": 5,
            "learning_rate": 0.1,
            "n_estimators": 100
        }
        
        # Log parameters
        mlflow.log_params(params)
        
        # 3. Train Model
        model = xgb.XGBClassifier(**params)
        model.fit(X_train, y_train)
        
        # 4. Evaluate
        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, preds)
        auc = roc_auc_score(y_test, probs)
        
        # Log metrics
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("roc_auc", auc)
        
        # 5. Log Model Artifact
        mlflow.xgboost.log_model(model, artifact_path="xgboost-model")
        print(f"Run completed. Accuracy: {acc}, AUC: {auc}")

if __name__ == "__main__":
    train_and_log_model()
