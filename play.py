import pandas as pd

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
NUM_ROUNDS = 5
CLOSE_ENOUGH_MPH = 3.0

def load_data():
    try:
        return pd.read_csv("data/joined.csv", parse_dates=["hour_ts"])
    except FileNotFoundError:
        print("No data found. Run 'python fetch_data.py' then 'python prepare_data.py' first.")
        raise SystemExit(1)

def get_guess(prompt):
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Please enter a number.")
            continue
        try:
            return float(raw)
        except ValueError:
            print(f"'{raw}' isn't a number — try again.")

def play_round(row, round_num):
    day_name = DAY_NAMES[row["day_of_week"]]
    date_str = row["hour_ts"].strftime("%B %d, %Y")
    time_str = row["hour_ts"].strftime("%I:%M %p").lstrip("0")

    print(f"\nRound {round_num} of {NUM_ROUNDS}")
    print(f"  Date:      {day_name}, {date_str}")
    print(f"  Time:      {time_str}")
    print(f"  Weather:   {row['temp_f']:.0f}°F, {row['precip_mm']:.1f}mm precip, wind {row['wind_mph']:.0f} mph")

    guess = get_guess("\nYour guess (avg speed, mph): ")
    actual = row["avg_speed_mph"]
    diff = abs(guess - actual)

    print(f"\n  You guessed:      {guess:.1f} mph")
    print(f"  Actual recorded:  {actual:.1f} mph")
    print(f"  Difference:       {diff:.1f} mph")

    if diff <= CLOSE_ENOUGH_MPH:
        print(f"  Nice — within {CLOSE_ENOUGH_MPH} mph! (+1 point)")
        return 1
    print("  Not quite (no point this round)")
    return 0

def main():
    df = load_data()
    print("=== Traffic Guess Game ===")
    print(f"{NUM_ROUNDS} rounds. Guess the average speed (mph) for each real historical hour.")

    sample = df.sample(n=NUM_ROUNDS).reset_index(drop=True)
    score = sum(play_round(row, i + 1) for i, row in sample.iterrows())
    print("-" * 40)
    print(f"\nFinal score: {score}/{NUM_ROUNDS}")

if __name__ == "__main__":
    main()