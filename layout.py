import dash_bootstrap_components as dbc
from dash import dcc, html
import graph_module as gm

class Layout:
    def __init__(self, app, df_athletes) -> None:
        self._df_athletes = df_athletes
        self._nor_athletes = df_athletes[df_athletes["NOC"] == "NOR"]
        self._sport_options = [{"label": sport, "value": sport} for sport in sorted(self._df_athletes["Sport"].unique())]


    def layout(self):
        start_content = dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(id="home-graph", figure=gm.most_medals_by_country(self._df_athletes)),
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(dcc.Graph(id="gender-distribution", figure=gm.gender_distribution(self._df_athletes))),
                                    dbc.Col(dcc.Graph(id="gender-distribution-by-games", figure=gm.gender_distribution_by_games(self._df_athletes))),
                                ]
                            ),
                        ]
                    )
                ]
            ),
            className="mt-3",
        )

        norway_content = dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(id="norway-participans", figure=gm.norwegian_participants_gender(self._nor_athletes)),
                    dcc.Graph(id="norway-decade", figure=gm.norwegian_medals_decade(self._nor_athletes)),
                    dcc.Graph(id="norway-age-boxplot", figure=gm.age_by_gender_by_year(self._nor_athletes)),
                    # dcc.Graph(id="norway-sports-colourful", figure=gm.norwegian_medals_sport_per_games(self._nor_athletes)),                          # obsolete when we have the graph below?
                    dcc.Graph(id="norway-sports-gender", figure=gm.medals_by_sport_and_gender(self._nor_athletes, "Norway's top performing sports")),
                    dcc.Graph(id="norway-medals", figure=gm.medal_coloured_bars(self._nor_athletes)),
                    dcc.Graph(id="norway-seasons", figure=gm.norwegian_medals_season(self._nor_athletes)),
                    dcc.Graph(id="norway-winter", figure=gm.top_medals_winter(self._df_athletes)),
                ]
            ),
            className="mt-3",
        )

        tab3_content = dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(id="medal-dist-subplot", figure=gm.subplot_medal_distribution(self._df_athletes, "Football","Gymnastics","Alpine Skiing","Shooting")),
                    dcc.Graph(id="sport-age-dist-graph", figure=gm.age_distribution_by_sports(self._df_athletes, ["Gymnastics","Shooting","Football","Alpine Skiing"]))

                ]
            ),
            className="mt-3",
        )

        sports_content = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([
                        dcc.Dropdown(id="dropdown-sports", options=self._sport_options, value="Football", clearable=False, style={"flex": "1"}),
                        html.Div([
                            dbc.Button(html.I(className="bi bi-caret-left"), id="dropdown-sports-left-btn", n_clicks=0),
                            dbc.Button(html.I(className="bi bi-caret-right"), id="dropdown-sports-right-btn", n_clicks=0),
                        ], style={"display": "flex", "gap": "0.25rem"}),
                    ], style={"display": "flex", "gap": "0.75rem"}),
                    dcc.Graph(id="sports-statistics-graph")
                ]
            ),
            className="mt-3",
        )


        tabs = dbc.Tabs(
            [
                dbc.Tab(start_content, label="Start"),
                dbc.Tab(norway_content, label="Norway"),
                dbc.Tab(tab3_content, label="Sport Selection"),
                dbc.Tab(sports_content, label="Sports"),
            ]
        )

        return dbc.Container([
            dbc.Card([
                dbc.CardBody([
                    html.Img(src="assets/olympic_games.png", style={"width": "54px", "objectFit": "cover", "height": "32px"}),
                    html.H4("Project Olympic Games", style={"margin": "0"}),
                ], style={"display": "flex", "alignItems": "center", "gap": "0.75rem"})
            ], style={"marginBottom": "1rem"}),
            tabs
        ])
    