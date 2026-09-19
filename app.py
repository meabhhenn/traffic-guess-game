import os
import json
import urllib.parse
import requests
import pandas as pd
from flask import Flask, render_template, request, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-key-not-for-production")

NUM_ROUNDS = 5
TIGHT_MPH = 1.0
LOOSE_MPH = 3.0
DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

MAPBOX_TOKEN = os.environ["MAPBOX_TOKEN"]
REGION_BOUNDS = {"west": -87.647208, "east": -87.62308, "south": 41.866129, "north": 41.88886}
_raw = pd.read_csv("data/traffic_raw.csv")
REGION_DESCRIPTION = _raw[_raw["region"] == "Chicago Loop"]["description"].iloc[0]
MAP_IMAGE_PATH = "static/region_map.png"

df = pd.read_csv("data/joined.csv", parse_dates=["hour_ts"])

OVERALL_MEAN_SPEED = df["avg_speed_mph"].mean()
OVERALL_MIN_SPEED = df["avg_speed_mph"].min()
OVERALL_MAX_SPEED = df["avg_speed_mph"].max()


def is_interesting(row):
    return (row["precip_mm"] > 0) or (row["wind_mph"] > 20) or (row["temp_f"] < 20) or (row["temp_f"] > 90)

df["weight"] = df.apply(lambda r: 3 if is_interesting(r) else 1, axis=1)

def build_map_if_needed():
    if os.path.exists(MAP_IMAGE_PATH):
        return
    os.makedirs("static", exist_ok=True)
    geojson = {
        "type": "Feature",
        "properties": {"stroke": "#ff3b30", "stroke-width": 3, "fill": "#ff3b30", "fill-opacity": 0.15},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [REGION_BOUNDS["west"], REGION_BOUNDS["south"]],
                [REGION_BOUNDS["east"], REGION_BOUNDS["south"]],
                [REGION_BOUNDS["east"], REGION_BOUNDS["north"]],
                [REGION_BOUNDS["west"], REGION_BOUNDS["north"]],
                [REGION_BOUNDS["west"], REGION_BOUNDS["south"]],
            ]],
        },
    }
    encoded = urllib.parse.quote(json.dumps(geojson))
    url = (
        f"https://api.mapbox.com/styles/v1/mapbox/streets-v12/static/"
        f"geojson({encoded})/auto/900x700?access_token={MAPBOX_TOKEN}"
        )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        with open(MAP_IMAGE_PATH, "wb") as f:
            f.write(resp.content)
    except requests.RequestException as e:
        print(f"Could not fetch map image, continuing without it: {e}")



build_map_if_needed()


def new_round_row():
    row = df.sample(n=1, weights=df["weight"]).to_dict("records")[0]
    return {
        "hour_ts": str(row["hour_ts"]),
        "avg_speed_mph": float(row["avg_speed_mph"]),
        "temp_f": float(row["temp_f"]),
        "precip_mm": float(row["precip_mm"]),
        "wind_mph": float(row["wind_mph"]),
        "day_of_week": int(row["day_of_week"]),
    }


def render_round(region_description=REGION_DESCRIPTION, error=None):
    current = session["current"]
    ts = pd.Timestamp(current["hour_ts"])
    return render_template(
        "round.html",
        round_num=session["round"],
        num_rounds=NUM_ROUNDS,
        score=session["score"],
        day_name=DAY_NAMES[current["day_of_week"]],
        day_type="Weekend" if current["day_of_week"] >= 5 else "Weekday",
        date_str=ts.strftime("%B %d, %Y"),
        time_str=ts.strftime("%I:%M %p").lstrip("0"),
        temp_f=current["temp_f"],
        precip_mm=current["precip_mm"],
        wind_mph=current["wind_mph"],
        map_available=os.path.exists(MAP_IMAGE_PATH),
        region_description=region_description,
        overall_mean_speed=OVERALL_MEAN_SPEED,
        overall_min_speed=OVERALL_MIN_SPEED,
        overall_max_speed=OVERALL_MAX_SPEED,
        error=error,
    )


@app.route("/")
def start_game():
    session["round"] = 1
    session["score"] = 0
    session["current"] = new_round_row()
    return render_round()


@app.route("/guess", methods=["POST"])
def guess():
    raw = request.form.get("guess", "").strip()
    if not raw:
        return render_round(error="Please enter a number.")
    try:
        guess_val = float(raw)
    except ValueError:
        return render_round(error=f"'{raw}' isn't a number — try again.")

    current = session["current"]
    actual = current["avg_speed_mph"]
    diff = abs(guess_val - actual)

    if diff <= TIGHT_MPH:
        points_earned = 3
    elif diff <= LOOSE_MPH:
        points_earned = 1
    else:
        points_earned = 0

    session["score"] += points_earned

    return render_template(
        "reveal.html",
        guess=guess_val,
        actual=actual,
        diff=diff,
        points_earned=points_earned,
        round_num=session["round"],
        num_rounds=NUM_ROUNDS,
        score=session["score"],
        is_last_round=session["round"] >= NUM_ROUNDS,
    )


@app.route("/next", methods=["POST"])
def next_round():
    if session.get("round", 0) >= NUM_ROUNDS:
        return render_round()  # safety net: don't advance past the last round
    session["round"] += 1
    session["current"] = new_round_row()
    return render_round()


if __name__ == "__main__":
    app.run(debug=True)