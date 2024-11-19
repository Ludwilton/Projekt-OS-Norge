import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, clientside_callback, ClientsideFunction
from dash_bootstrap_components._components.Container import Container
import plotly_express as px
import pandas as pd
from data_utils import group_medals, filter_medal_entries

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


def update_norway_medals_per_year_graph(df):
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
        plot_bgcolor="white"
    )

    return fig


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


def update_norway_graph(df):
    df = df
    df = df[df["NOC"] == "NOR"]
    medal_counts = group_medals(df, "Sport")

    medal_counts = medal_counts[medal_counts["Total"] > 0]

    return px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title="Sporter där Norge tagit flest medaljer")


def update_home_graph(df):
    df = df

    medal_counts = group_medals(df, "NOC")

    medal_counts = medal_counts[medal_counts["Total"] > 0]

    # Get top 20 countries by total amount of medals
    medal_counts = medal_counts.sort_values(by="Total", ascending=False)
    medal_counts = medal_counts.iloc[:20]

    return px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title="Länder som tagit flest medaljer")


class Layout:
    def __init__(self, app, df_athletes) -> None:
        self._app = app

        self._df_athletes = df_athletes
        self._athletes_dict = {"Diving": "Dykning", "Football": "Fotboll", "Gymnastics": "Gymnastik", "Swimming": "Simning"}

        self._sport_options = [{"label": name, "value": symbol}
                        for symbol, name in self._athletes_dict.items()]


    def layout(self):
        tab1_content = dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(id="home-graph", figure=update_home_graph(self._df_athletes)),
                    dcc.Dropdown(id="dropdown_sports", options=self._sport_options, value="Football"),
                    dcc.Graph(id="medals-per-sport-graph"),
                ]
            ),
            className="mt-3",
        )

        tab2_content = dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(id="norway-graph", figure=update_norway_graph(self._df_athletes)),
                    dcc.Graph(id="norway-medals-per-year-graph", figure=update_norway_medals_per_year_graph(self._df_athletes)),
                    dcc.Graph(id="norway-age-histogram", figure=update_norway_age_histogram(self._df_athletes))
                ]
            ),
            className="mt-3",
        )

        tab3_content = dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(id="sport-age-dist-graph", figure=update_sport_age_dist_graph(self._df_athletes))
                ]
            ),
            className="mt-3",
        )


        tabs = dbc.Tabs(
            [
                dbc.Tab(tab1_content, label="Hem"),
                dbc.Tab(tab2_content, label="Norge"),
                dbc.Tab(tab3_content, label="Knapp"),
            ]
        )

        return tabs
    