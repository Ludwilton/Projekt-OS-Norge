import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc
from dash_bootstrap_components._components.Container import Container

class Layout:
    def __init__(self, app) -> None:
        self._app = app
        # self._app.callback(Output("main-div", "children"), Input("btn_home", "n_clicks"))(self.btn_home_click)
        # self._app.callback(Output("main-div", "children"), Input("btn_norway", "n_clicks"))(self.btn_norway_click)
        
    def btn_home_click(self, n_clicks):
        if n_clicks == 0:
            return
            
        print("click")

        return self.get_home_layout()

    def btn_norway_click(self, n_clicks):
        if n_clicks == 0:
            return
        
        print("click")

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
            dbc.Container(
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
    