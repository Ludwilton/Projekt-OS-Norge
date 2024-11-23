import pandas as pd
import matplotlib.pyplot as plt
import hashlib as hl
import seaborn as sns
import plotly_express as px 

def read_athlete_events(file_path = "athlete_events.csv") -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df


def filter_medal_entries(df: pd.DataFrame):
    df_medal_entries = df[df["Medal"].notnull()]
    df_medal_entries = df_medal_entries.drop_duplicates(subset=["Event", "Games", "Team", "Medal"])
    return df_medal_entries


def group_medals(df: pd.DataFrame, group_by="NOC"):
    df_medals = df.copy()
    df_medals["Medal"] = df_medals["Medal"].fillna("No Medal")
    df_medals = df_medals.drop_duplicates(subset=["Event", "Games", "Team", "Medal"])
    medal_counts = df_medals.groupby([group_by, "Medal"]).size().unstack(fill_value=0)
    for medal in ["Bronze", "Silver", "Gold"]:                                              # fixes KeyError if there are no medals of a certain type
        if medal not in medal_counts.columns:
            medal_counts[medal] = 0
    medal_counts["Total"] = medal_counts[["Bronze", "Silver", "Gold"]].sum(axis=1)
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
    TODO fix settingwithcopywarning
    anonymizes specified column on passed df
    drops specified column
    returns modified df
    '''
    hashed_column= df[column].apply(lambda row_value: hl.sha256(row_value.encode()).hexdigest())
    df.insert(1,"Hash", hashed_column)
    df = df.drop(columns=[column])
    return df



def get_NOC_color():     # används för konsistent unik färg på varje land
    df = read_athlete_events()
    countries = df["NOC"].unique()
    palette = px.colors.qualitative.Light24                                 # gpt
    palette_cycle = palette * (len(countries) // len(palette) + 1)          # gpt
    country_colors = dict(zip(countries, palette_cycle[:len(countries)]))   # gpt
    return country_colors




if __name__ == "__main__":
    df = pd.read_csv("athlete_events.csv")
    
    # medals_by_country = group_medals(df, group_by="NOC")
    # print(medals_by_country)

    # df_norway = df[df["NOC"] == "NOR"]
    # norway_medals_per_sport = group_medals(df_norway, group_by="Sport")
    # print(norway_medals_per_sport)

    plot_top_medals(df)


