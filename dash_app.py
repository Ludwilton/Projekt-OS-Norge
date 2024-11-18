import dash_bootstrap_components as dbc
from dash import Input, Output, State, html, dcc, clientside_callback, ClientsideFunction
from dash_bootstrap_components._components.Container import Container
import plotly_express as px
import pandas as pd
from data_utils import group_medals, filter_medal_entries

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
        
        self._app.callback(
            Output("sport-age-dist-graph", "figure"),
            Input("btn_new", "n_clicks_timestamp"),
        )(self.update_sport_age_dist_graph)

        self._app.callback(
            Output("norway-medals-per-year-graph", "figure"),
            Input("btn_norway", "n_clicks_timestamp")
        )(self.update_norway_medals_per_year_graph)

        self._app.callback(
            Output("norway-age-histogram", "figure"),
            Input("btn_norway", "n_clicks_timestamp")
        )(self.update_norway_age_histogram)
        

    def update_norway_age_histogram(self, norway_clicked_time):
        norway_athletes = self._df_athletes[self._df_athletes["NOC"] == "NOR"]

        fig = px.histogram(
            norway_athletes, 
            x="Age", 
            color="Sex"
        )

        fig.update_layout(barmode='overlay')
        fig.update_traces(opacity=0.75)

        return fig


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
    

    def update_sport_age_dist_graph(self, value_sport):
        
        df = self._df_athletes.dropna(subset=["Age"])

        df_filt = df.drop_duplicates(subset=["Sport", "Games", "ID"])
        sports = ["Gymnastics","Shooting","Football","Alpine Skiing"] # TODO, make a dropdown to add or remove sports for easy comparision
        df_filt = df_filt[df_filt["Sport"].isin(sports)]


        return px.box(
            df_filt,
            x="Sport",
            y="Age",
            title="Medelålder per sport",
            labels={"Age": "ålders-fördelning (år)", "Sport": "Sport"},
            color="Sport", 
        )
    
# ----- TODO
    # def age_distribution_sports_graph(self, value_sports):
    #     df_all_unique_participants = self._df_athletes.drop_duplicates(subset=["ID"])
    #     df_age_distribution_sports = df_all_unique_participants[df_all_unique_participants["Sport"].isin(["Alpine Skiing", "Gymnastics", "Football", "Shooting"])]

    #     medals_by_country = df_age_distribution_sports.groupby(["NOC", "Sport"])["Medal"].count().reset_index()
    #     all_medals_df = medals_by_country[medals_by_country["Medal"] > 0]
    #     df_dist_ = all_medals_df[all_medals_df["Sport"]== "Alpine Skiing"].sort_values(by="Medal", ascending=False)


    #     # plt.figure(figsize=(10,5))
    #     # sns.barplot(shooting_medals, x="NOC", y="Medal", hue="NOC")
    #     # plt.title("Shooting medals")
    #     # plt.xticks(rotation=90)
    #     # plt.tight_layout()
    #     # plt.show()

    #     return px.box(
    #         df_filt,
    #         x="Sport",
    #         y="Age",
    #         title="Medelålder per sport",
    #         labels={"Age": "ålders-fördelning (år)", "Sport": "Sport"},
    #         color="Sport", 
    #     )

    def update_norway_medals_per_year_graph(self, norway_clicked_time):
        df_norway_medals = filter_medal_entries(self._df_athletes[self._df_athletes["NOC"] == "NOR"])

        def prepare_medal_data(df, category_label):
            medal_count = group_medals(df, "Year").sort_values(by="Year")
            medal_count = medal_count.reset_index()
            medal_count["Category"] = category_label
            return medal_count


        medal_count_all = prepare_medal_data(df_norway_medals, "Overall")
        medal_count_wom = prepare_medal_data(df_norway_medals[df_norway_medals["Sex"] == "F"], "Women")
        medal_count_men = prepare_medal_data(df_norway_medals[df_norway_medals["Sex"] == "M"], "Men")

        plot_data = pd.concat([medal_count_all, medal_count_wom, medal_count_men])

        fig = px.line(
            plot_data,
            x="Year",
            y="Total",
            color="Category",
            title="Norwegian Olympic medals",
            labels={"Total": "Number of medals", "Year": "Year"},
            color_discrete_map={"Overall": "crimson", "Men": "forestgreen", "Women": "orange"}
        )

        fig.update_layout(
            title={"text": "Norwegian Olympic medals", "x": 0.5, "xanchor": "center"},
            yaxis_title="Number of medals",
            xaxis_title="Year",
            legend_title_text="Category",
            plot_bgcolor="white"
        )

        return fig


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
                    dcc.Graph(id="norway-graph"),
                    dcc.Graph(id="norway-medals-per-year-graph"),
                    dcc.Graph(id="norway-age-histogram")
                ], id="norway-content", style={ "display": "none", "position": "relative" }),
                dbc.Container([
                    dcc.Graph(id="sport-age-dist-graph")
                ], id="new-content", style={ "display": "none", "position": "relative" }),
            ], id="main-div")
        ], style={"padding": "0"})
    