import plotly_express as px
from data_utils import group_medals, filter_medal_entries
import pandas as pd
import matplotlib.pyplot as plt

athletes_dict = {"Diving": "Dykning", "Football": "Fotboll", "Gymnastics": "Gymnastik", "Swimming": "Simning"}
sport_options = [{"label": name, "value": symbol} for symbol, name in athletes_dict.items()]


def update_norway_age_histogram(df):
    norway_athletes = df[df["NOC"] == "NOR"]

    fig = px.histogram(
        norway_athletes, 
        x="Age", 
        color="Sex"
    )

    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75)

    return fig


def update_per_sport_graph(sport, df):

    df_sport = df[df["Sport"] == sport]

    medal_counts = group_medals(df_sport)

    medal_counts = medal_counts[medal_counts["Total"] > 0]

    # Get top 20 countries by total amount of medals
    medal_counts = medal_counts.sort_values(by="Total", ascending=False)
    medal_counts = medal_counts.iloc[:20]

    fig = px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title=athletes_dict[sport])
    return fig


def update_home_graph(df):

    medal_counts = group_medals(df, "NOC")

    medal_counts = medal_counts[medal_counts["Total"] > 0]

    # Get top 20 countries by total amount of medals
    medal_counts = medal_counts.sort_values(by="Total", ascending=False)
    medal_counts = medal_counts.iloc[:20]

    return px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title="Länder som tagit flest medaljer")


def update_norway_graph(df):
    df = df[df["NOC"] == "NOR"]
    medal_counts = group_medals(df, "Sport")

    medal_counts = medal_counts[medal_counts["Total"] > 0]

    return px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title="Sporter där Norge tagit flest medaljer")


def update_sport_age_dist_graph(df):
    
    df = df.dropna(subset=["Age"])

    df_filt = df.drop_duplicates(subset=["Sport", "Games", "ID"])
    sports = ["Gymnastics","Shooting","Football","Alpine Skiing"] # TODO, make a dropdown to add or remove sports for easy comparision
    df_filt = df_filt[df_filt["Sport"].isin(sports)]


    return px.box(
        df_filt,
        x="Sport",
        y="Age",
        title="Medelålder per sport",
        labels={"Age": "ålders-fördelning (år)", "Sport": "Sport"},
        color="Sport", 
    )

# ----- TODO
def age_distribution_sports_graph(df, sport="Alpine Skiing"):
    df_all_unique_participants = df.drop_duplicates(subset=["ID"])
    df_age_distribution_sports = df_all_unique_participants[df_all_unique_participants["Sport"].isin(["Alpine Skiing", "Gymnastics", "Football", "Shooting"])]

    medals_by_country = df_age_distribution_sports.groupby(["NOC", "Sport"])["Medal"].count().reset_index()
    all_medals_df = medals_by_country[medals_by_country["Medal"] > 0]
    df_dist_ = all_medals_df[all_medals_df["Sport"]== sport].sort_values(by="Medal", ascending=False)

    return px.bar(df_dist_, x="NOC", y="Medal", color="NOC")



def update_norway_medals_per_year_graph(self, norway_clicked_time):
    df_norway_medals = filter_medal_entries(self._df_athletes[self._df_athletes["NOC"] == "NOR"])

    def prepare_medal_data(df, category_label):
        medal_count = group_medals(df, "Year").sort_values(by="Year")
        medal_count = medal_count.reset_index()
        medal_count["Category"] = category_label
        return medal_count


    medal_count_all = prepare_medal_data(df_norway_medals, "Overall")
    medal_count_wom = prepare_medal_data(df_norway_medals[df_norway_medals["Sex"] == "F"], "Women")
    medal_count_men = prepare_medal_data(df_norway_medals[df_norway_medals["Sex"] == "M"], "Men")

    plot_data = pd.concat([medal_count_all, medal_count_wom, medal_count_men])

    fig = px.line(
        plot_data,
        x="Year",
        y="Total",
        color="Category",
        title="Norwegian Olympic medals",
        labels={"Total": "Number of medals", "Year": "Year"},
        color_discrete_map={"Overall": "crimson", "Men": "forestgreen", "Women": "orange"}
    )

    fig.update_layout(
        title={"text": "Norwegian Olympic medals", "x": 0.5, "xanchor": "center"},
        yaxis_title="Number of medals",
        xaxis_title="Year",
        legend_title_text="Category",
        plot_bgcolor="white"
    )

    return fig


if __name__ == "__main__":
    df = pd.read_csv("athlete_events.csv")
 
    fig = age_distribution_sports_graph(df)