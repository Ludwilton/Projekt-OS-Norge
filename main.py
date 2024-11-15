import dash
from dash_app import Dash_App
import dash_bootstrap_components as dbc
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

df_athletes = pd.read_csv("athlete_events.csv")

dash_app = Dash_App(app, df_athletes)
app.layout = dash_app.layout()
dash_app.define_callbacks()

if __name__ == '__main__':
    app.run_server(debug=True)