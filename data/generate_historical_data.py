"""
Generates synthetic historical disaster records for training the severity prediction AI model.
Includes multi-hazard features for floods, cyclones, earthquakes, and landslides.
"""

import os
import numpy as np
import pandas as pd

def generate_historical_dataset(n_samples: int = 1500, random_state: int = 42) -> pd.DataFrame:
    """Generates a realistic synthetic dataset for disaster severity modeling."""
    np.random.seed(random_state)

    disaster_types = np.random.choice(["Flood", "Cyclone", "Earthquake", "Landslide"], size=n_samples, p=[0.35, 0.25, 0.20, 0.20])

    data = []
    for d_type in disaster_types:
        # Base environmental metrics
        if d_type == "Flood":
            rainfall = np.random.uniform(50, 450)          # mm / 24h
            flood_level = np.random.uniform(0.5, 6.5)       # meters above danger mark
            wind_speed = np.random.uniform(15, 65)          # km/h
            soil_saturation = np.random.uniform(70, 100)    # %
            magnitude = 0.0
            slope_angle = np.random.uniform(1, 15)          # degrees
        elif d_type == "Cyclone":
            rainfall = np.random.uniform(80, 500)
            flood_level = np.random.uniform(0.2, 4.0)
            wind_speed = np.random.uniform(75, 220)         # km/h
            soil_saturation = np.random.uniform(60, 95)
            magnitude = 0.0
            slope_angle = np.random.uniform(1, 20)
        elif d_type == "Earthquake":
            rainfall = np.random.uniform(0, 80)
            flood_level = 0.0
            wind_speed = np.random.uniform(5, 30)
            soil_saturation = np.random.uniform(10, 60)
            magnitude = np.random.uniform(4.5, 8.2)         # Richter
            slope_angle = np.random.uniform(5, 45)
        else: # Landslide
            rainfall = np.random.uniform(100, 400)
            flood_level = np.random.uniform(0.0, 1.5)
            wind_speed = np.random.uniform(10, 45)
            soil_saturation = np.random.uniform(80, 100)
            magnitude = np.random.uniform(0.0, 3.5)
            slope_angle = np.random.uniform(25, 65)         # steep slope

        pop_density = np.random.uniform(300, 12000)        # people / sq km
        infra_quality = np.random.uniform(2.0, 9.0)        # 10 = indestructible, 2 = fragile
        bridge_cutoff = np.random.choice([0, 1], p=[0.65, 0.35])
        dist_to_hub_km = np.random.uniform(5, 60)

        # Synthetic ground truth severity calculation (1.0 to 10.0 scale)
        if d_type == "Flood":
            hazard_intensity = (rainfall / 450.0) * 4.0 + (flood_level / 6.5) * 4.5
        elif d_type == "Cyclone":
            hazard_intensity = (wind_speed / 220.0) * 5.0 + (rainfall / 500.0) * 3.5
        elif d_type == "Earthquake":
            hazard_intensity = ((magnitude - 4.0) / 4.2) * 8.5
        else: # Landslide
            hazard_intensity = (slope_angle / 65.0) * 4.0 + (soil_saturation / 100.0) * 2.5 + (rainfall / 400.0) * 2.0

        vulnerability = (10.0 - infra_quality) * 0.25 + (pop_density / 12000.0) * 1.5 + (bridge_cutoff * 1.0)
        noise = np.random.normal(0, 0.35)

        raw_severity = (hazard_intensity * 0.65) + (vulnerability * 0.35) + noise
        severity = float(np.clip(raw_severity, 1.0, 10.0))

        # Risk tier
        if severity >= 7.8:
            risk_category = "Critical Emergency"
        elif severity >= 5.5:
            risk_category = "High Severity"
        elif severity >= 3.5:
            risk_category = "Moderate Impact"
        else:
            risk_category = "Low Impact"

        data.append({
            "disaster_type": d_type,
            "rainfall_24h_mm": round(rainfall, 1),
            "flood_water_level_m": round(flood_level, 2),
            "wind_speed_kmh": round(wind_speed, 1),
            "soil_saturation_pct": round(soil_saturation, 1),
            "richter_magnitude": round(magnitude, 1),
            "slope_angle_deg": round(slope_angle, 1),
            "population_density_sqkm": round(pop_density, 0),
            "infrastructure_quality": round(infra_quality, 1),
            "bridge_cutoff": int(bridge_cutoff),
            "dist_to_hub_km": round(dist_to_hub_km, 1),
            "severity_score": round(severity, 2),
            "risk_category": risk_category
        })

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    out_dir = os.path.dirname(__file__)
    csv_path = os.path.join(out_dir, "historical_disaster_data.csv")
    df = generate_historical_dataset(1500)
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(df)} synthetic historical disaster records to {csv_path}")
