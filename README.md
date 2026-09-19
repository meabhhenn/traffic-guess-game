# Traffic Guess Game

A small Flask web game that tests your intuition for real Chicago traffic patterns. Each round shows real historical weather and time-of-day conditions for a specific hour in downtown Chicago (the traffic speed is hidden), and you guess the average recorded vehicle speed for that hour. The app reveals what actually happened and scores your guess.

## How the APIs are used

Traffic data comes from the City of Chicago's Traffic Tracker API (a keyless Socrata REST endpoint), queried with `requests` using a `$where` clause that filters by region name and a date range; it returns JSON records with fields like `time`, `region`, and `speed`. Historical weather comes from Open-Meteo's Historical Weather API (also keyless), queried with latitude/longitude and a date range, returning hourly JSON arrays for temperature, precipitation, and wind speed. The two are joined locally with pandas by rounding each traffic reading down to its containing hour and merging on that hour. A region map image is fetched once from Mapbox's Static Images API (requires a free API key) and cached to disk rather than re-fetched on every page load.

## API key setup

Only Mapbox requires a key. Sign up for a free account at mapbox.com, copy your "Default public token" from your account page, and create a file named `.env` in the project root containing:

```
MAPBOX_TOKEN=your_token_here
```

`.env` is excluded from the repo via `.gitignore` — never commit it.

## Running it

```
pip install -r requirements.txt
python fetch_data.py      # pulls raw traffic + weather data (run once)
python prepare_data.py    # joins them into data/joined.csv
python app.py             # starts the game at http://127.0.0.1:5000
```
