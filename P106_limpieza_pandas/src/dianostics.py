import pandas as pd
from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = ACTIVITY_DIR / "data" / "ventas.csv"
OUTPUT_FILE = ACTIVITY_DIR / "submission" / "ventas.csv"


def main():

#######################################
    df = pd.read_csv(OUTPUT_FILE)
    series = df['supplier']
    series = series.drop_duplicates()
    series = series.sort_values(ascending=True)
    for value in series:
        print(repr(value))

if __name__ == "__main__":
    main()
