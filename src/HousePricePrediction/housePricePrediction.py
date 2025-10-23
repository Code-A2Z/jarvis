"""
housePricePrediction.py

"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Path to a tiny sample CSV included in the folder (commit a very small sample)
DATA_PATH = os.path.join(os.path.dirname(__file__), "examples", "sample_house_data.csv")


def load_data(path=DATA_PATH):
    if not os.path.exists(path):
        print(f"[ERROR] Dataset not found at {path}. Include a small 'examples/sample_house_data.csv' (see README).")
        return None
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"[ERROR] Could not read CSV: {e}")
        return None
    if df.empty:
        print("[ERROR] CSV loaded but it's empty.")
        return None
    return df


def infer_target_and_features(df):
    """
    Decide target (y) and features (X) defensively:
    - If 'SalePrice' exists, use it as target.
    - Otherwise, try to use the last numeric column as target.
    """
    df = df.copy()
    if "SalePrice" in df.columns:
        y_name = "SalePrice"
    else:
        # pick last numeric column as fallback
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if not numeric_cols:
            print("[ERROR] No numeric columns found in dataset to use as target.")
            return None, None
        y_name = numeric_cols[-1]

    if y_name not in df.columns:
        print(f"[ERROR] Target column {y_name} not found.")
        return None, None

    X = df.drop(columns=[y_name])
    y = df[y_name]
    if X.shape[1] == 0:
        print("[ERROR] No feature columns available after dropping target.")
        return None, None
    return X, y


def build_pipeline(numeric_cols, categorical_cols):
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    # Use sparse=False for compatibility with older sklearn; acceptable for small OHE results.
    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse=False))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipeline, numeric_cols),
        ("cat", categorical_pipeline, categorical_cols)
    ])
    return preprocessor


def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = mean_squared_error(y_test, preds, squared=False)
    r2 = r2_score(y_test, preds)
    return {"MAE": mae, "RMSE": rmse, "R2": r2}


def housePricePrediction():
    """Main entrypoint — name matches file per contributing rules."""
    df = load_data()
    if df is None:
        return

    X, y = infer_target_and_features(df)
    if X is None or y is None:
        return

    # Simple heuristic for numeric vs categorical columns
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = [c for c in X.columns if c not in numeric_cols]

    # Build preprocessor
    preprocessor = build_pipeline(numeric_cols, categorical_cols)

    # split
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    except Exception as e:
        print(f"[ERROR] Could not split data: {e}")
        return

    # Model 1: Linear Regression (baseline)
    try:
        lr_pipeline = Pipeline([
            ("pre", preprocessor),
            ("model", LinearRegression())
        ])
        lr_pipeline.fit(X_train, y_train)
        lr_metrics = evaluate_model(lr_pipeline, X_test, y_test)
        print("LinearRegression metrics:", lr_metrics)
    except Exception as e:
        print(f"[WARN] LinearRegression failed: {e}")

    # Model 2: Random Forest
    try:
        rf_pipeline = Pipeline([
            ("pre", preprocessor),
            ("model", RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
        ])
        rf_pipeline.fit(X_train, y_train)
        rf_metrics = evaluate_model(rf_pipeline, X_test, y_test)
        print("RandomForest metrics:", rf_metrics)
        # Save the model locally (do NOT commit this file). PR should NOT include this file.
        joblib.dump(rf_pipeline, "house_price_model_joblib.pkl")
        print("Saved model to house_price_model_joblib.pkl (do NOT commit).")
    except Exception as e:
        print(f"[WARN] RandomForest failed: {e}")


if __name__ == "__main__":
    housePricePrediction()
