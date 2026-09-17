import pandas as pd

traffic_df = pd.read_csv("data/traffic_raw.csv")
weather_df = pd.read_csv("data/weather_raw.csv")

# Parse timestamps and floor traffic readings down to the hour
traffic_df["time"] = pd.to_datetime(traffic_df["time"])
traffic_df["hour_ts"] = traffic_df["time"].dt.floor("h")
traffic_df["speed"] = pd.to_numeric(traffic_df["speed"], errors="coerce")

# Collapse multiple readings per hour into one average speed
hourly_traffic = (
    traffic_df.groupby("hour_ts")["speed"]
    .mean()
    .reset_index()
    .rename(columns={"speed": "avg_speed_mph"})
)

# Parse weather timestamps (already exactly hourly)
weather_df["hour_ts"] = pd.to_datetime(weather_df["time"])
weather_df["temp_f"] = weather_df["temperature_2m"] * 9 / 5 + 32
weather_df["wind_mph"] = weather_df["windspeed_10m"] * 0.621371
weather_df = weather_df.rename(columns={"precipitation": "precip_mm"})

# Join on the shared hour timestamp
joined = pd.merge(
    hourly_traffic,
    weather_df[["hour_ts", "temp_f", "precip_mm", "wind_mph"]],
    on="hour_ts",
    how="inner",
)

# Derive time features directly from the timestamp, not the original API fields,
# so hour/day-of-week/month are guaranteed consistent with hour_ts itself
joined["hour"] = joined["hour_ts"].dt.hour
joined["day_of_week"] = joined["hour_ts"].dt.dayofweek  # Monday=0 ... Sunday=6
joined["month"] = joined["hour_ts"].dt.month

joined = joined.dropna()
joined.to_csv("data/joined.csv", index=False)
print(f"Joined dataset: {len(joined)} rows")
print(joined.head())