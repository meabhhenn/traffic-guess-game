import os, json, urllib.parse, requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ["MAPBOX_TOKEN"]

# Replaced with region's real values from the lookup above
west, east, south, north = -87.647208, -87.62308, 41.866129, 41.88886
geojson = {
    "type": "Feature",
    "properties": {"stroke": "#ff3b30", "stroke-width": 3, "fill": "#ff3b30", "fill-opacity": 0.15},
    "geometry": {
        "type": "Polygon",
        "coordinates": [[[west, south], [east, south], [east, north], [west, north], [west, south]]],
    },
}
encoded = urllib.parse.quote(json.dumps(geojson))

url = (
    f"https://api.mapbox.com/styles/v1/mapbox/streets-v12/static/"
    f"geojson({encoded})/auto/600x400?access_token={TOKEN}"
)

resp = requests.get(url)
resp.raise_for_status()
with open("test_map.png", "wb") as f:
    f.write(resp.content)
print("Saved test_map.png")