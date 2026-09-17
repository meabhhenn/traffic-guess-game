import requests

# 1. Look at a few raw Chicago traffic records
chicago_resp = requests.get(
    "https://data.cityofchicago.org/resource/kf7e-cur8.json",
    params={"$limit": 5}
)
chicago_resp.raise_for_status()
print("Sample Chicago traffic rows:")
print(chicago_resp.json())

# 2. Get the full list of distinct region names this dataset uses
regions_resp = requests.get(
    "https://data.cityofchicago.org/resource/kf7e-cur8.json",
    params={"$select": "distinct region", "$limit": 50}
)
regions_resp.raise_for_status()
print("\nAvailable regions:")
print(regions_resp.json())

# 3. Look at a raw Open-Meteo weather response for Chicago, 2 days
weather_resp = requests.get(
    "https://archive-api.open-meteo.com/v1/archive",
    params={
        "latitude": 41.8781,
        "longitude": -87.6298,
        "start_date": "2024-01-01",
        "end_date": "2024-01-02",
        "hourly": "temperature_2m,precipitation,windspeed_10m",
        "timezone": "America/Chicago",
    }
)
weather_resp.raise_for_status()
print("\nSample Open-Meteo weather response:")
print(weather_resp.json())