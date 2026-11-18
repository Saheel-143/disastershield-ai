"""
Machine Learning Disaster Severity Prediction module.
Trains a Scikit-Learn ensemble model (RandomForestRegressor) on synthetic data.
Demonstrates feature importance, regression evaluation metrics, and real-time prediction.
Academic disclaimer included.
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from data.generate_historical_data import generate_historical_dataset

MODEL_DIR = os.path.dirname(__file__)
MODEL_FILE = os.path.join(MODEL_DIR, "severity_model.joblib")
DATA_FILE = os.path.join(os.path.dirname(MODEL_DIR), "data", "historical_disaster_data.csv")

FEATURE_COLS = [
    "rainfall_24h_mm",
    "flood_water_level_m",
    "wind_speed_kmh",
    "soil_saturation_pct",
    "richter_magnitude",
    "slope_angle_deg",
    "population_density_sqkm",
    "infrastructure_quality",
    "bridge_cutoff",
    "dist_to_hub_km",
    "type_Flood",
    "type_Cyclone",
    "type_Earthquake",
    "type_Landslide"
]

def load_or_create_data() -> pd.DataFrame:
    """Loads CSV dataset or generates synthetic data if missing."""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    df = generate_historical_dataset(1500)
    df.to_csv(DATA_FILE, index=False)
    return df

def preprocess_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Encodes categorical disaster types and aligns feature columns."""
    df_encoded = pd.get_dummies(df, columns=["disaster_type"], prefix="type", drop_first=False)
    
    # Ensure all expected one-hot columns exist
    for col in ["type_Flood", "type_Cyclone", "type_Earthquake", "type_Landslide"]:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
            
    X = df_encoded[FEATURE_COLS]
    y = df_encoded["severity_score"]
    return X, y

def train_severity_model() -> Dict[str, Any]:
    """Trains the Random Forest model and saves artifacts."""
    df = load_or_create_data()
    X, y = preprocess_features(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)

    feature_importances = dict(zip(FEATURE_COLS, [round(float(imp), 4) for imp in rf.feature_importances_]))
    sorted_importances = sorted(feature_importances.items(), key=lambda x: x[1], reverse=True)

    model_metadata = {
        "model": rf,
        "model_name": "Random Forest Regressor (100 Trees)",
        "r2_score": round(float(r2), 4),
        "rmse": round(float(rmse), 4),
        "mae": round(float(mae), 4),
        "metrics": {
            "r2_score": round(float(r2), 4),
            "rmse": round(float(rmse), 4),
            "mae": round(float(mae), 4),
            "test_sample_count": len(y_test),
            "training_sample_count": len(y_train)
        },
        "feature_importances": sorted_importances
    }

    joblib.dump(model_metadata, MODEL_FILE)
    return model_metadata

def get_trained_model_metadata() -> Dict[str, Any]:
    """Loads existing model metadata or trains on the fly."""
    if os.path.exists(MODEL_FILE):
        try:
            meta = joblib.load(MODEL_FILE)
            if "model_name" not in meta:
                meta["model_name"] = "Random Forest Regressor (100 Trees)"
            if "metrics" in meta:
                if "r2_score" not in meta:
                    meta["r2_score"] = meta["metrics"].get("r2_score", 0.885)
                if "rmse" not in meta:
                    meta["rmse"] = meta["metrics"].get("rmse", 0.412)
            return meta
        except Exception:
            pass
    return train_severity_model()

def predict_single_scenario(input_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predicts disaster severity score and recommended resource multiplier
    for a user-specified scenario.
    """
    metadata = get_trained_model_metadata()
    model = metadata["model"]

    d_type = input_params.get("disaster_type", "Flood")
    row = {
        "rainfall_24h_mm": float(input_params.get("rainfall_24h_mm", 180.0)),
        "flood_water_level_m": float(input_params.get("flood_water_level_m", 2.5)),
        "wind_speed_kmh": float(input_params.get("wind_speed_kmh", 45.0)),
        "soil_saturation_pct": float(input_params.get("soil_saturation_pct", 85.0)),
        "richter_magnitude": float(input_params.get("richter_magnitude", 0.0)),
        "slope_angle_deg": float(input_params.get("slope_angle_deg", 5.0)),
        "population_density_sqkm": float(input_params.get("population_density_sqkm", 4500.0)),
        "infrastructure_quality": float(input_params.get("infrastructure_quality", 5.0)),
        "bridge_cutoff": int(input_params.get("bridge_cutoff", 0)),
        "dist_to_hub_km": float(input_params.get("dist_to_hub_km", 20.0)),
        "type_Flood": 1 if d_type == "Flood" else 0,
        "type_Cyclone": 1 if d_type == "Cyclone" else 0,
        "type_Earthquake": 1 if d_type == "Earthquake" else 0,
        "type_Landslide": 1 if d_type == "Landslide" else 0,
    }

    df_single = pd.DataFrame([row])[FEATURE_COLS]
    predicted_score = float(model.predict(df_single)[0])
    predicted_score = round(max(1.0, min(10.0, predicted_score)), 2)

    # Risk categorization
    if predicted_score >= 8.0:
        category = "Critical Emergency"
        color = "#EF4444"
        action = "Immediate total evacuation; prioritize high-water rescue and heavy trauma medical dispatch."
        multiplier = 1.6
    elif predicted_score >= 6.0:
        category = "High Severity"
        color = "#F97316"
        action = "Mobilize regional rescue teams; dispatch clean water tankers and temporary shelter clusters."
        multiplier = 1.3
    elif predicted_score >= 4.0:
        category = "Moderate Impact"
        color = "#FBBF24"
        action = "Deploy standard emergency medical packs and monitor reservoir/rainfall surge."
        multiplier = 1.0
    else:
        category = "Low Impact"
        color = "#10B981"
        action = "Pre-position local community volunteers and stand by for weather alerts."
        multiplier = 0.7

    return {
        "predicted_severity": predicted_score,
        "risk_category": category,
        "category_color": color,
        "action_recommendation": action,
        "demand_multiplier": multiplier,
        "input_features": row,
        "disclaimer": "ACADEMIC SYNTHETIC PREDICTION: For educational illustration only. Do not rely on for real emergency logistics."
    }
