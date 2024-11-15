import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
from dash_bootstrap_components._components.Container import Container

class Layout:
    def __init__(self, app) -> None:
        self._app = app

        self._app.callback(
            Output("main-div", "children"),
            Input("btn_home", "n_clicks_timestamp"),
            Input("btn_norway", "n_clicks_timestamp")
        )(self.uppdatera_innehall)

    def uppdatera_innehall(self, hem_time, norge_time):
        print("hem_time", hem_time)
        print("norge_time", norge_time)

        if hem_time is None and norge_time is None:
            return self.get_home_layout()

        if hem_time is not None and (norge_time is None or hem_time > norge_time):
            return self.get_home_layout()
        elif norge_time is not None and (hem_time is None or norge_time > hem_time):
            return self.get_norway_layout()


    def get_norway_layout(self):
        return html.Div([
            "Norge"
        ])
    
    def get_home_layout(self):
        return html.Div([
            "Hem"
        ])

    def layout(self):
        navbar = dbc.Navbar(
            html.Div(
                [
                    dbc.Button("Hem", id="btn_home", className="navbar_button", n_clicks=0),
                    dbc.Button("Norge", id="btn_norway", className="navbar_button", n_clicks=0),
                ]
            ),
            color="dark",
            dark=True,
        )

        return dbc.Container([
            navbar,
            html.Div([], id="main-div")
        ])
    