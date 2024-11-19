import dash
from dash import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from layout import Layout
import graph_module as gm

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

df_athletes = pd.read_csv("athlete_events.csv")

app.layout = Layout(app, df_athletes).layout()

@app.callback(
    Output("medals-per-sport-graph", "figure"),
    Input("dropdown_sports", "value"),
)
def handle_dropdown_sports_change(value):
    return gm.sport_subplots(df_athletes, sport=value)


if __name__ == '__main__':
    app.run_server(debug=True)