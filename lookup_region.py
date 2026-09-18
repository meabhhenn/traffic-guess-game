import pandas as pd
df = pd.read_csv("data/traffic_raw.csv")
print(df[["region", "west", "east", "south", "north"]].drop_duplicates())