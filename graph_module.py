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
        color="Sex",
        title="Age distribution by gender"
    )

    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75, marker_line_width=1.5)

    return fig


def countries_with_most_medals_in_sport(df, sport, subplot=False):
    if subplot:
        df_sport = df
    else:
        df_sport = df[df["Sport"] == sport]


    medal_counts = group_medals(df_sport)

    medal_counts = medal_counts[medal_counts["Total"] > 0]

    # Get top 20 countries by total amount of medals
    medal_counts = medal_counts.sort_values(by="Total", ascending=False)
    medal_counts = medal_counts.iloc[:20]

    if subplot:
        num_colors = len(df["NOC"])
        colors = px.colors.qualitative.Plotly * (num_colors // len(px.colors.qualitative.Plotly) + 1) # gpt
        return go.Bar(
            x=medal_counts.index,
            y=medal_counts["Total"],
            name=sport,
            marker=dict(color=colors[:num_colors])
        )
    else:
        fig = px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title=sport, color=medal_counts.index)

        return fig


def age_distribution_of_one_sport(df, sport, subplot=False):
    # TODO: Male och Female måste alltid ha samma färg oavsett om det är flest Male eller Female

    if subplot:
        df_sport = df
    else:
        df_sport = df[df["Sport"] == sport]

    if subplot: 
        # TODO: Kunna se andel Male och Female i grafen
        trace = go.Histogram(
            x=df_sport["Age"],
            name=sport,
            marker_color=px.colors.qualitative.Plotly[0]
        )
        return trace
    else:
        fig = px.histogram(df_sport, x="Age", color="Sex", barmode="overlay", title="Average age of Norwegian Olympic athletes", labels={"Age": "Age", "Sex": "Gender"})

        fig.update_layout(barmode='overlay')
        fig.update_traces(opacity=0.75, marker_line_width=1.5)
        
        return fig


def sport_subplots(df, sport):
    df_sport = df[df["Sport"] == sport]
    fig = make_subplots(rows=2, cols=2, subplot_titles=["Medal Distribution by Country", "Age Distribution", "", ""])
    fig.add_trace(countries_with_most_medals_in_sport(df_sport, sport, subplot=True), row=1, col=1)
    fig.add_trace(age_distribution_of_one_sport(df_sport, sport, subplot=True), row=1, col=2) 
    # fig.add_trace(countries_with_most_medals_in_sport(df_sport, sport=sport, subplot=True), row=2, col=1)
    # fig.add_trace(countries_with_most_medals_in_sport(df_sport, sport=sport, subplot=True), row=2, col=2)
    fig.update_layout(title=f"Statistics for {sport}", showlegend=False)
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



def age_distribution_by_sports(df, sports = ["Gymnastics","Shooting","Football","Alpine Skiing"]): 

    df = df.dropna(subset=["Age"])

    df_filt = df.drop_duplicates(subset=["Sport", "Games", "ID"])

    df_filt = df_filt[df_filt["Sport"].isin(sports)]

    fig = px.box(
        df_filt,
        x="Sport",
        y="Age",
        title="Age distribution by sports",
        labels={"Age": "Agr distribution (years)", "Sport": "Sport"},
        color="Sport"
    )
    fig.update_layout(showlegend = False)
    
    return fig


def medal_distribution_by_country(df, sport="Alpine Skiing", subplot=False): 
    
    df_all_unique_participants = df.drop_duplicates(subset=["ID"])
    medals_by_country = df_all_unique_participants.groupby(["NOC", "Sport"])["Medal"].count().reset_index()
    all_medals_df = medals_by_country[medals_by_country["Medal"] > 0]
    df_dist_ = all_medals_df[all_medals_df["Sport"]== sport].sort_values(by="Medal", ascending=False)
    
    if subplot:
        num_colors = len(df_dist_["NOC"]) # gpt
        colors = px.colors.qualitative.Plotly * (num_colors // len(px.colors.qualitative.Plotly) + 1) # gpt
        return go.Bar(
        x=df_dist_["NOC"],
        y=df_dist_["Medal"],
        name=sport,
        marker=dict(color=colors[:num_colors])
    )
    else:
        return px.bar(df_dist_, x="NOC", y="Medal", color="NOC", labels={"Medal": "Medals"}, title=f"Medal distribution in {sport}")
    
        

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


def age_by_gender_by_year(df):
    no_df = df[df["NOC"]=="NOR"]
    fig = px.box(
        no_df,
        x="Year",
        y="Age",
        color="Sex",
        points=False,
        title="Age distribution by gender per year"

    )
    fig.update_layout()
    return fig

# TODO add title to 3rd graph norway page


def gender_distribution(df: pd.DataFrame):
    gender_counts = df["Sex"].value_counts().reset_index()
    gender_counts.columns = ["Sex", "Count"]

    fig = px.bar(
        gender_counts,
        x="Sex",
        y="Count",
        title="Gender Distribution",
        labels={"Sex": "Sex", "Count": "Number of Participants"},
        color="Sex",
    )

    return fig


def gender_distribution_by_games(df: pd.DataFrame):
    dist_by_games = df.groupby("Games")["Sex"].value_counts().reset_index()

    fig = px.histogram(dist_by_games, x="Games", y="count", color='Sex', barmode='group')
    
    fig.update_layout(
        title={"text": "Gender Distribution By Games"},
        yaxis_title="Number of Participants",
        xaxis_title="Games",
        legend_title_text="Sex",
    )

    return fig


def events_per_game(df: pd.DataFrame):
    df = df.drop_duplicates(subset=["Event", "Games"])

    events_per_game = df.groupby("Games")["Event"].value_counts().reset_index()

    fig = px.histogram(events_per_game, x="Games", y="count")
    
    fig.update_layout(
        title={"text": "Events Per Game"},
        yaxis_title="Number of Events",
        xaxis_title="Games"
    )

    return fig
