import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, clientside_callback, ClientsideFunction
from dash_bootstrap_components._components.Container import Container
import plotly_express as px
from data_utils import group_medals

class Dash_App:
    def __init__(self, app, df_athletes) -> None:
        self._app = app

        self._df_athletes = df_athletes
        self._athletes_dict = {"Diving": "Dykning", "Football": "Fotboll", "Gymnastics": "Gymnastik", "Swimming": "Simning"}

        self._sport_options = [{"label": name, "value": symbol}
                        for symbol, name in self._athletes_dict.items()]

        clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_main_content'
            ),
            Input("btn_home", "n_clicks_timestamp"),
            Input("btn_norway", "n_clicks_timestamp"),
            Input("btn_new", "n_clicks_timestamp"),
        )
        
        
    def define_callbacks(self):
        self._app.callback(
            Output("home-graph", "figure"),
            Input("btn_home", "n_clicks_timestamp"),
        )(self.update_home_graph)

        self._app.callback(
            Output("medals-per-sport-graph", "figure"),
            Input("dropdown_sports", "value"),
        )(self.update_per_sport_graph)

        self._app.callback(
            Output("norway-graph", "figure"),
            Input("btn_norway", "n_clicks_timestamp")
        )(self.update_norway_graph)
        

    def update_per_sport_graph(self, sport):
        df = self._df_athletes

        df_sport = df[df["Sport"] == sport]

        medal_counts = group_medals(df_sport)

        medal_counts = medal_counts[medal_counts["Total"] > 0]

        # Get top 20 countries by total amount of medals
        medal_counts = medal_counts.sort_values(by="Total", ascending=False)
        medal_counts = medal_counts.iloc[:20]

        fig = px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title=self._athletes_dict[sport])
        return fig
    

    def update_home_graph(self, home_clicked_time):
        df = self._df_athletes

        medal_counts = group_medals(df, "NOC")

        medal_counts = medal_counts[medal_counts["Total"] > 0]

        # Get top 20 countries by total amount of medals
        medal_counts = medal_counts.sort_values(by="Total", ascending=False)
        medal_counts = medal_counts.iloc[:20]

        return px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title="Länder som tagit flest medaljer")


    def update_norway_graph(self, norway_clicked_time):
        df = self._df_athletes
        df = df[df["NOC"] == "NOR"]
        medal_counts = group_medals(df, "Sport")

        medal_counts = medal_counts[medal_counts["Total"] > 0]

        return px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title="Sporter där Norge tagit flest medaljer")
    

    def layout(self):
        navbar = dbc.Navbar(
            html.Div(
                [
                    dbc.Button("Hem", id="btn_home", className="navbar_button", n_clicks=0),
                    dbc.Button("Norge", id="btn_norway", className="navbar_button", n_clicks=0),
                    dbc.Button("Knapp", id="btn_new", className="navbar_button", n_clicks=0),
                ]
            ),
            color="dark",
            dark=True,
        )

        return dbc.Container([
            navbar,
            html.Div([
                dbc.Container([
                    dcc.Graph(id="home-graph"),
                    dcc.Dropdown(id="dropdown_sports", options=self._sport_options, value="Football"),
                    dcc.Graph(id="medals-per-sport-graph"),
                ], id="home-content"),
                dbc.Container([
                    html.Img(src="../assets/norwegian_flag.jpg", id="norway-flag"),
                    dcc.Graph(id="norway-graph")
                ], id="norway-content", style={ "display": "none", "position": "relative" }),
                dbc.Container([
                    "Här lägger vi grafer med mera"
                ], id="new-content", style={ "display": "none", "position": "relative" }),
            ], id="main-div")
        ], style={"padding": "0"})
    