import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import plotly_express as px
import pandas as pd
from data_utils import group_medals
from layout import Layout
import dash_bootstrap_components as dbc

df_athletes = pd.read_csv("athlete_events.csv")
athletes_dict = {"Diving": "Dykning", "Football": "Fotboll", "Gymnastics": "Gymnastik", "Swimming": "Simning"}

sport_options = [{"label": name, "value": symbol}
                 for symbol, name in athletes_dict.items()]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = Layout(app).layout()


# @app.callback(
#     Output("sport-graph", "figure"),
#     Input("sport-picker-dropdown", "value")
# )
# def update_graph(sport):
#     df_sport = df_athletes[df_athletes["Sport"] == sport]

#     data = group_medals(df_sport)

#     data = data[data.Total > 0]

#     fig = px.bar(data, x=data.index, y=data.Total, title=athletes_dict[sport])
#     return fig


if __name__ == '__main__':
    app.run_server(debug=True)