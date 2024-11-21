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
def update_dropdown(left_n_clicks, right_n_clicks, current_value, options):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_value
    
    # Get the id of the element that triggered the callback
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    dropdown_option_values = [option["value"] for option in options]

    # Find the index of the currently chosen value in dropdown from the options
    current_index = dropdown_option_values.index(current_value)

    if button_id == "dropdown-sports-left-btn":
        # If left button is clicked select option above the current selected (previous index)
        new_index = (current_index - 1) % len(dropdown_option_values)
    elif button_id == "dropdown-sports-right-btn":
        # If right button is clicked select option below the current selected (next index)
        new_index = (current_index + 1) % len(dropdown_option_values)
    else:
        new_index = current_index

    # Return the value to the dropdown by the new index
    return dropdown_option_values[new_index]


if __name__ == '__main__':
    app.run_server(debug=True)