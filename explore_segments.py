import requests

west, east, south, north = -87.647208, -87.62308, 41.866129, 41.88886

resp = requests.get(
    "https://data.cityofchicago.org/resource/4g9f-3jbs.json",
    params={
        "$where": (
            f"start_latitude between {south} and {north} "
            f"AND start_longitude between {west} and {east} "
            f"AND time between '2024-06-01T00:00:00' and '2024-06-01T23:59:59'"
        ),
        "$limit": 5000,
    }
)
resp.raise_for_status()
data = resp.json()
print(f"Rows returned for one day: {len(data)}")

streets = sorted({row.get("street") for row in data})
print(f"Distinct streets found: {streets}")

segments = {(row.get("street"), row.get("from_street"), row.get("to_street")) for row in data}
print(f"Distinct segments: {len(segments)}")
for seg in sorted(segments):
    print(seg)