import pandas as pd

def read_athlete_events(file_path = "athlete_events.csv") -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df


if __name__ == "__main__":
    df = read_athlete_events()
    print(df)