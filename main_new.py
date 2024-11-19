import dash
from dash import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly_express as px
from layout import Layout
from data_utils import group_medals

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

df_athletes = pd.read_csv("athlete_events.csv")

athletes_dict = {"Diving": "Dykning", "Football": "Fotboll", "Gymnastics": "Gymnastik", "Swimming": "Simning"}

app.layout = Layout(app, df_athletes).layout()

@app.callback(
    Output("medals-per-sport-graph", "figure"),
    Input("dropdown_sports", "value"),
)
def update_per_sport_graph(sport):
    df = df_athletes

    df_sport = df[df["Sport"] == sport]

    medal_counts = group_medals(df_sport)

    medal_counts = medal_counts[medal_counts["Total"] > 0]

    # Get top 20 countries by total amount of medals
    medal_counts = medal_counts.sort_values(by="Total", ascending=False)
    medal_counts = medal_counts.iloc[:20]

    fig = px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title=athletes_dict[sport])
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)