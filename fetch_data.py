import requests
import pandas as pd

REGION = "Chicago Loop"  
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"

# --- Chicago traffic data ---
traffic_resp = requests.get(
    "https://data.cityofchicago.org/resource/kf7e-cur8.json",
    params={
        "$where": f"region='{REGION}' AND time between '{START_DATE}T00:00:00' and '{END_DATE}T23:59:59'",
        "$order": "time",
        "$limit": 50000,
    }
)
traffic_resp.raise_for_status()
traffic_df = pd.DataFrame(traffic_resp.json())
print(f"Traffic rows fetched: {len(traffic_df)}")

# --- Open-Meteo historical weather ---
weather_resp = requests.get(
    "https://archive-api.open-meteo.com/v1/archive",
    params={
        "latitude": 41.8781,
        "longitude": -87.6298,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "hourly": "temperature_2m,precipitation,windspeed_10m",
        "timezone": "America/Chicago",
    }
)
weather_resp.raise_for_status()
weather_df = pd.DataFrame(weather_resp.json()["hourly"])
print(f"Weather rows fetched: {len(weather_df)}")

traffic_df.to_csv("data/traffic_raw.csv", index=False)
weather_df.to_csv("data/weather_raw.csv", index=False)
print("Saved raw data to data/traffic_raw.csv and data/weather_raw.csv")