import plotly_express as px
from data_utils import group_medals, filter_medal_entries
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def norway_age_histogram(df):
    norway_athletes = df[df["NOC"] == "NOR"]
 
    fig = px.histogram(
        norway_athletes, 
        x="Age", 
        color="Sex"
    )

    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75, marker_line_width=1.5)

    return fig


def countries_with_most_medals_in_sport(df, sport):
    df_sport = df[df["Sport"] == sport]

    medal_counts = group_medals(df_sport)

    medal_counts = medal_counts[medal_counts["Total"] > 0]

    # Get top 20 countries by total amount of medals
    medal_counts = medal_counts.sort_values(by="Total", ascending=False)
    medal_counts = medal_counts.iloc[:20]

    fig = px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title=sport, color=medal_counts.index)
    return fig


def most_medals_by_country(df):

    medal_counts = group_medals(df, "NOC")

    medal_counts = medal_counts[medal_counts["Total"] > 0]

    # Get top 20 countries by total amount of medals
    medal_counts = medal_counts.sort_values(by="Total", ascending=False)
    medal_counts = medal_counts.iloc[:20]

    return px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title="Countries with most amount of medals", color=medal_counts.index, color_discrete_sequence=px.colors.qualitative.Light24)


def norway_top_sports(df):
    df = df[df["NOC"] == "NOR"]
    medal_counts = group_medals(df, "Sport")

    medal_counts = medal_counts[medal_counts["Total"] > 0]

    return px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title="Sports with most amount of medals by Norway", color=medal_counts.index, color_discrete_sequence=px.colors.qualitative.Light24)


def age_distribution_by_sports(df):
    df = df.dropna(subset=["Age"])

    df_filt = df.drop_duplicates(subset=["Sport", "Games", "ID"])
    sports = ["Gymnastics","Shooting","Football","Alpine Skiing"] # TODO, make a dropdown to add or remove sports for easy comparision
    df_filt = df_filt[df_filt["Sport"].isin(sports)]


    return px.box(
        df_filt,
        x="Sport",
        y="Age",
        title="Age distribution by sports",
        labels={"Age": "Agr distribution (years)", "Sport": "Sport"},
        color="Sport", 
    )


# ----- TODO fix graph function name
def medal_distribution_by_country(df, sport="Alpine Skiing", subplot=False): 
    df_all_unique_participants = df.drop_duplicates(subset=["ID"])
    df_age_distribution_sports = df_all_unique_participants[df_all_unique_participants["Sport"].isin(["Alpine Skiing", "Gymnastics", "Football", "Shooting"])]

    medals_by_country = df_age_distribution_sports.groupby(["NOC", "Sport"])["Medal"].count().reset_index()
    all_medals_df = medals_by_country[medals_by_country["Medal"] > 0]
    df_dist_ = all_medals_df[all_medals_df["Sport"]== sport].sort_values(by="Medal", ascending=False)
    if subplot == False:
        return px.bar(df_dist_, x="NOC", y="Medal", color="NOC", labels={"Medal": "Medals"}, title=f"Medal distribution in {sport}")
    elif subplot == True:
        num_colors = len(df_dist_["NOC"])
        colors = px.colors.qualitative.Plotly * (num_colors // len(px.colors.qualitative.Plotly) + 1)
        return go.Bar(
        x=df_dist_["NOC"],
        y=df_dist_["Medal"],
        name=sport,
        marker=dict(color=colors[:num_colors])
    )
        

def subplot_medal_distribution(df, sport1, sport2, sport3, sport4):
    fig = make_subplots(rows=2, cols=2, subplot_titles=[sport1, sport2, sport3, sport4])
    fig.add_trace(medal_distribution_by_country(df, sport=sport1, subplot=True), row=1, col=1)
    fig.add_trace(medal_distribution_by_country(df, sport=sport2, subplot=True), row=1, col=2)
    fig.add_trace(medal_distribution_by_country(df, sport=sport3, subplot=True), row=2, col=1)
    fig.add_trace(medal_distribution_by_country(df, sport=sport4, subplot=True), row=2, col=2)
    fig.update_layout(title=f"Medal Distribution by Country for {sport1}, {sport2}, {sport3}, {sport4}", showlegend=False)
    return fig


def norway_medals_per_year(df):
    df_norway_medals = filter_medal_entries(df[df["NOC"] == "NOR"])

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
    )

    return fig