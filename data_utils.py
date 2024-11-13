import pandas as pd
import matplotlib.pyplot as plt

def read_athlete_events(file_path = "athlete_events.csv") -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df


def group_medals(df: pd.DataFrame, group_by="NOC"):
    df_medals = df.dropna(subset=["Medal"])

    medal_counts = df_medals.groupby([group_by, "Medal"]).size().unstack(fill_value=0)

    medal_counts["Total"] = medal_counts.sum(axis=1)

    medal_counts = medal_counts.reindex(columns=['Bronze', 'Silver', 'Gold', 'Total'])

    medal_counts = medal_counts.sort_values(by="Total", ascending=False)

    return medal_counts


def plot_top_medals(df: pd.DataFrame, limit=10, group_by='NOC'):
    # Filtrera bort rader utan medaljer
    df_medals = df.dropna(subset=['Medal'])

    medal_counts = df_medals.groupby(["NOC", "Medal"]).size().unstack(fill_value=0)
    print(medal_counts)
    return

    # df_medals = df_medals[df_medals["Sport"] == "Football"]

    medal_count = df_medals[group_by].value_counts()

    # Välj de 10 länderna med flest medaljer
    top_10_countries = medal_count.sort_values(ascending=False).head(limit)

    # Skapa grafen
    plt.figure(figsize=(10, 6))
    top_10_countries.plot(kind='bar', color='skyblue')
    plt.title('Topp 10 länder med flest OS-medaljer')
    plt.xlabel('Land (NOC)')
    plt.ylabel('Totalt antal medaljer')
    plt.xticks(rotation=45)
    plt.show()


if __name__ == "__main__":
    df = pd.read_csv("athlete_events.csv")
    
    medals_by_country = group_medals(df, group_by="NOC")
    print(medals_by_country)

    df_norway = df[df["NOC"] == "NOR"]
    norway_medals_per_sport = group_medals(df_norway, group_by="Sport")
    print(norway_medals_per_sport)