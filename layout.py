import dash_bootstrap_components as dbc
from dash import dcc
import graph_module as gm

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
                    dcc.Graph(id="home-graph", figure=gm.update_home_graph(self._df_athletes)),
                    
                    dcc.Dropdown(id="dropdown_sports", options=self._sport_options, value="Football"),
                    dcc.Graph(id="medals-per-sport-graph"),
                ]
            ),
            className="mt-3",
        )

        tab2_content = dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(id="norway-graph", figure=gm.update_norway_graph(self._df_athletes)),
                    dcc.Graph(id="norway-medals-per-year-graph", figure=gm.update_norway_medals_per_year_graph(self._df_athletes)),
                    dcc.Graph(id="norway-age-histogram", figure=gm.update_norway_age_histogram(self._df_athletes))
                ]
            ),
            className="mt-3",
        )

        tab3_content = dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(id="sport-age-dist-graph", figure=gm.update_sport_age_dist_graph(self._df_athletes))
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
    