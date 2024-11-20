import dash
from dash import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from layout import Layout
import graph_module as gm

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

server = app.server

df_athletes = pd.read_csv("athlete_events.csv")

app.layout = Layout(app, df_athletes).layout()

@app.callback(
    Output("medals-per-sport-graph", "figure"),
    Input("dropdown-sports", "value"),
)
def handle_dropdown_sports_change(value):
    return gm.sport_subplots(df_athletes, sport=value)


@app.callback(
    Output("dropdown-sports", "value"),
    Input("dropdown-sports-left-btn", "n_clicks"),
    Input("dropdown-sports-right-btn", "n_clicks"),
    State("dropdown-sports", "value"),
    State("dropdown-sports", "options")
)
def update_dropdown(left_clicks, right_clicks, current_value, options):
    dropdown_option_values = [option["value"] for option in options]
    
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_value
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    current_index = dropdown_option_values.index(current_value)

    if button_id == "dropdown-sports-left-btn":
        new_index = (current_index - 1) % len(dropdown_option_values)
    elif button_id == "dropdown-sports-right-btn":
        new_index = (current_index + 1) % len(dropdown_option_values)
    else:
        new_index = current_index

    return dropdown_option_values[new_index]


if __name__ == '__main__':
    app.run_server(debug=True)