import pandas as pd
import matplotlib.pyplot as plt
import hashlib as hl
import seaborn as sns
import plotly_express as px 
import math


def read_athlete_events(file_path = "athlete_events.csv") -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df = hash_column(df, "Name")

    return df


def group_medals(df: pd.DataFrame, group_by="NOC"):
    df_medals = df.copy()
    df_medals["Medal"] = df_medals["Medal"].fillna("No Medal")

    # Drop duplicates ensures that team medals count as one medal
    df_medals = df_medals.drop_duplicates(subset=["Event", "Games", "Team", "Medal"])

    medal_counts = df_medals.groupby([group_by, "Medal"]).size().unstack(fill_value=0)

    # If count for the medal type is missing, set 0 to the column
    for medal in ["Bronze", "Silver", "Gold"]:
        if medal not in medal_counts.columns:
            medal_counts[medal] = 0

    medal_counts["Total"] = medal_counts[["Bronze", "Silver", "Gold"]].sum(axis=1)

    # Set the columns in correct order for graph purposes, and sort the medal counts by the Total
    medal_counts = medal_counts.reindex(columns=["Bronze", "Silver", "Gold", "Total"])
    medal_counts = medal_counts.sort_values(by="Total", ascending=False)

    return medal_counts


def plot_top_medals(df: pd.DataFrame, limit=10, group_by='NOC') -> None:
    medal_counts = group_medals(df, group_by)

    medal_counts = medal_counts.head(limit)
    ax = sns.barplot(medal_counts, y="Total", x=group_by, hue=group_by)
    for container in ax.containers:
        ax.bar_label(container)

    plt.show()


def hash_column(df, column): 
    '''
    anonymizes specified column on passed df
    drops specified column
    returns modified df
    '''
    hashed_column= df[column].apply(lambda row_value: hl.sha256(row_value.encode()).hexdigest())
    df.insert(1,"Hash", hashed_column)
    df = df.drop(columns=[column])
    return df


def get_NOC_color():
    '''
    Used for consistent color for every country.
    '''
    df = read_athlete_events()

    # Chat GPT is used for this solution.
    # "I want to dynamically assign unique colors to each country in my DataFrame column NOC for a Plotly bar chart. 
    # Provide a method to generate a unique color palette based on the unique values of NOC, 
    # ensuring consistent and distinct colors for all countries,
    #  and integrate it into my medal_distribution_by_country function."
    # *code for medal_distribution_by_country function*
    countries = df["NOC"].unique()
    palette = px.colors.qualitative.Light24                                 # gpt
    palette_cycle = palette * (len(countries) // len(palette) + 1)          # gpt
    country_colors = dict(zip(countries, palette_cycle[:len(countries)]))   # gpt

    return country_colors


def round_down_to_nearest_ten(number):
    return math.floor(number / 10) * 10


def round_up_to_nearest_ten(number):
    return math.ceil(number / 10) * 10


if __name__ == "__main__":
    df = read_athlete_events()
    plot_top_medals(df)
