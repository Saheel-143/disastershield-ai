"""
Free Open-Source API Integrations for DisasterShield AI.
Integrates free public APIs requiring NO API KEYS, NO SUBSCRIPTIONS, and NO MANDATORY CLOUD SERVICES:
1. Open-Meteo Weather & Flood API (https://open-meteo.com/) - Live meteorological and precipitation telemetry.
2. USGS Earthquake Hazards Program API (https://earthquake.usgs.gov/) - Real-time global seismic disaster feed.
3. OpenStreetMap Nominatim Geocoding API (https://nominatim.openstreetmap.org/) - Free place name coordinate lookup.
All functions include graceful offline/timeout fallbacks.
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional

OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"
USGS_EARTHQUAKE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

DEFAULT_HEADERS = {
    "User-Agent": "DisasterShield-AI/1.0 (Academic Decision-Support Prototype; CSDX 507; sahee.academic@gmail.com)"
}

def fetch_live_weather_telemetry(latitude: float, longitude: float, timeout_sec: int = 5) -> Dict[str, Any]:
    """
    Fetches live real-time meteorological conditions from Open-Meteo Free API (Zero API key required).
    Returns real precipitation (rainfall mm), wind speed (km/h), humidity, and atmospheric pressure.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,precipitation,rain,wind_speed_10m,surface_pressure",
        "hourly": "precipitation_probability",
        "forecast_days": 1,
        "timezone": "auto"
    }

    try:
        resp = requests.get(OPEN_METEO_BASE_URL, params=params, headers=DEFAULT_HEADERS, timeout=timeout_sec)
        if resp.status_code == 200:
            data = resp.json()
            curr = data.get("current", {})
            return {
                "success": True,
                "api_source": "Open-Meteo Free Meteorological API (No Key Required)",
                "timestamp": curr.get("time", time.strftime("%Y-%m-%dT%H:%M")),
                "temperature_c": curr.get("temperature_2m", 28.0),
                "rainfall_current_mm": curr.get("precipitation", 0.0),
                "rain_mm": curr.get("rain", 0.0),
                "wind_speed_kmh": curr.get("wind_speed_10m", 15.0),
                "humidity_pct": curr.get("relative_humidity_2m", 75),
                "surface_pressure_hpa": curr.get("surface_pressure", 1012.0),
                "latitude": latitude,
                "longitude": longitude
            }
    except Exception as e:
        pass

    # Graceful Offline Fallback
    return {
        "success": False,
        "api_source": "Offline Fallback Simulation (Network Timeout)",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M"),
        "temperature_c": 27.5,
        "rainfall_current_mm": 18.5,
        "rain_mm": 18.5,
        "wind_speed_kmh": 42.0,
        "humidity_pct": 88,
        "surface_pressure_hpa": 1008.0,
        "latitude": latitude,
        "longitude": longitude
    }


def fetch_usgs_live_earthquakes(min_magnitude: float = 4.0, limit: int = 10, timeout_sec: int = 6) -> List[Dict[str, Any]]:
    """
    Fetches real-time global earthquake feeds from USGS Earthquake Hazards Program (Free, No Key).
    """
    params = {
        "format": "geojson",
        "minmagnitude": min_magnitude,
        "limit": limit,
        "orderby": "time"
    }

    try:
        resp = requests.get(USGS_EARTHQUAKE_URL, params=params, headers=DEFAULT_HEADERS, timeout=timeout_sec)
        if resp.status_code == 200:
            data = resp.json()
            features = data.get("features", [])
            results = []
            for f in features:
                props = f.get("properties", {})
                geom = f.get("geometry", {})
                coords = geom.get("coordinates", [0, 0, 0])

                results.append({
                    "id": f.get("id"),
                    "place": props.get("place", "Unknown Location"),
                    "magnitude": round(float(props.get("mag", 0.0)), 1),
                    "time_epoch_ms": props.get("time"),
                    "time_str": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(props.get("time", 0) / 1000.0)) if props.get("time") else "Recent",
                    "depth_km": round(float(coords[2]), 1) if len(coords) > 2 else 10.0,
                    "longitude": float(coords[0]),
                    "latitude": float(coords[1]),
                    "tsunami_alert": bool(props.get("tsunami", 0)),
                    "significance": props.get("sig", 0),
                    "url": props.get("url", "https://earthquake.usgs.gov")
                })
            return results
    except Exception:
        pass

    # Fallback static sample if network blocked
    return [
        {
            "id": "usgs_sample_1",
            "place": "12 km W of Hindukush Mountain Ridge",
            "magnitude": 6.8,
            "time_str": "2026-10-31 08:42 UTC",
            "depth_km": 24.5,
            "longitude": 70.82,
            "latitude": 36.45,
            "tsunami_alert": False,
            "significance": 680,
            "url": "https://earthquake.usgs.gov"
        },
        {
            "id": "usgs_sample_2",
            "place": "Off Coast of Northern Sumatra, Indonesia",
            "magnitude": 5.9,
            "time_str": "2026-10-30 19:15 UTC",
            "depth_km": 32.0,
            "longitude": 96.12,
            "latitude": 3.84,
            "tsunami_alert": True,
            "significance": 520,
            "url": "https://earthquake.usgs.gov"
        }
    ]


def geocode_location_nominatim(query: str, timeout_sec: int = 5) -> Optional[Dict[str, Any]]:
    """
    Free Nominatim OpenStreetMap location search (No API key required).
    Resolves human place name to latitude and longitude.
    """
    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }
    try:
        resp = requests.get(NOMINATIM_URL, params=params, headers=DEFAULT_HEADERS, timeout=timeout_sec)
        if resp.status_code == 200:
            data = resp.json()
            if data and len(data) > 0:
                first = data[0]
                return {
                    "display_name": first.get("display_name"),
                    "latitude": float(first.get("lat")),
                    "longitude": float(first.get("lon"))
                }
    except Exception:
        pass
    return None
