import plotly_express as px
from data_utils import group_medals, filter_medal_entries, get_NOC_color
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

pd.options.mode.copy_on_write = True        # as to avoid a Pandas FutureWarning

country_colors = get_NOC_color()  # TODO i dont like having this as a global variable, should declare this inside every function that uses it instead


def round_down_to_nearest_ten(number):
    return math.floor(number / 10) * 10


def round_up_to_nearest_ten(number):
    return math.ceil(number / 10) * 10


def sport_subplots(df: pd.DataFrame, sport):
    df_sport = df[df["Sport"] == sport]
    gender_colors = {"M": "blue", "F": "red"}

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            "Top Medal-Winning Countries",
            "Age Distribution",
            "Gender Distribution",
            "Body Metrics of Athletes",
        ]
    )

    def countries_with_most_medals_in_sport():
        medal_counts = group_medals(df_sport)
        medal_counts = medal_counts[medal_counts["Total"] > 0].sort_values(
            by="Total", ascending=False
        ).iloc[:20]

        return go.Bar(
            x=medal_counts.index,
            y=medal_counts["Total"],
            name="Medals",
            marker=dict(
                color=[
                    country_colors.get(country, "#000000")
                    for country in medal_counts.index
                ]
            ),
        )


    def age_distribution_by_gender():
        traces = []

        for gender, color in gender_colors.items():
            df_gender = df_sport[df_sport["Sex"] == gender]
            traces.append(
                go.Histogram(
                    x=df_gender["Age"],
                    name="Male" if gender == "M" else "Female",
                    marker_color=color,
                    opacity=0.7,
                )
            )
        return traces


    def gender_distribution_of_sport():
        gender_counts = df_sport["Sex"].value_counts().reindex(["M", "F"], fill_value=0)

        return go.Bar(
            x=["Male", "Female"],
            y=gender_counts.values,
            marker_color=["blue", "red"],
            name="Participants",
        )


    def height_and_weight_correlation():
        return go.Scatter(
            x=df_sport["Weight"],
            y=df_sport["Height"],
            mode="markers",
            marker=dict(color=df_sport["Sex"].map(gender_colors)),
            name="Athletes",
        )


    fig.add_trace(countries_with_most_medals_in_sport(), row=1, col=1)
    for trace in age_distribution_by_gender():
        fig.add_trace(trace, row=1, col=2)
    fig.add_trace(gender_distribution_of_sport(), row=2, col=1)
    fig.add_trace(height_and_weight_correlation(), row=2, col=2)

    min_height = round_down_to_nearest_ten(df["Height"].min())
    max_height = round_up_to_nearest_ten(df["Height"].max())
    min_weight = round_down_to_nearest_ten(df["Weight"].min())
    max_weight = round_up_to_nearest_ten(df["Weight"].max())
    min_age = round_down_to_nearest_ten(df["Age"].min())
    max_age = round_up_to_nearest_ten(df["Age"].max())

    fig.update_xaxes(title_text="Country (NOC)", row=1, col=1)
    fig.update_yaxes(title_text="Number of Medals", row=1, col=1)

    fig.update_xaxes(title_text="Age", range=[min_age, max_age], row=1, col=2)
    fig.update_yaxes(title_text="Number of Participants", row=1, col=2)

    fig.update_xaxes(title_text="Gender", row=2, col=1)
    fig.update_yaxes(title_text="Number of Participants", row=2, col=1)

    fig.update_xaxes(title_text="Weight (kg)", range=[min_weight, max_weight], row=2, col=2)
    fig.update_yaxes(title_text="Height (cm)", range=[min_height, max_height], row=2, col=2)

    fig.update_layout(
        title=f"Statistics for {sport}",
        showlegend=False,
        height=800,
        margin=dict(l=50, r=50, t=100, b=50),
    )

    return fig


def most_medals_by_country(df):

    medal_counts = group_medals(df, "NOC")

    medal_counts = medal_counts[medal_counts["Total"] > 0]

    # Get top 20 countries by total amount of medals
    medal_counts = medal_counts.sort_values(by="Total", ascending=False)
    medal_counts = medal_counts.iloc[:20]

    return px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title="Countries with most amount of medals", color=medal_counts.index, color_discrete_sequence=px.colors.qualitative.Light24)


def norway_top_sports(df):
    df = df[df["NOC"] == "NOR"]
    medal_counts = group_medals(df, "Sport")

    medal_counts = medal_counts[medal_counts["Total"] > 0]

    return px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title="Sports with most amount of medals by Norway", color=medal_counts.index, color_discrete_sequence=px.colors.qualitative.Light24)



def age_distribution_by_sports(df, sports = ["Gymnastics","Shooting","Football","Alpine Skiing"]): 

    df = df.dropna(subset=["Age"])

    df_filt = df.drop_duplicates(subset=["Sport", "Games", "ID"])

    df_filt = df_filt[df_filt["Sport"].isin(sports)]

    fig = px.box(
        df_filt,
        x="Sport",
        y="Age",
        title="Age distribution by sports",
        labels={"Age": "Agr distribution (years)", "Sport": "Sport"},
        color="Sport"
    )
    fig.update_layout(showlegend = False)
    
    return fig


def medal_distribution_by_country(df, sport="Alpine Skiing", subplot=False): 
    
    df_all_unique_participants = df.drop_duplicates(subset=["ID"])
    medals_by_country = df_all_unique_participants.groupby(["NOC", "Sport"])["Medal"].count().reset_index()
    all_medals_df = medals_by_country[medals_by_country["Medal"] > 0]
    df_dist_ = all_medals_df[all_medals_df["Sport"]== sport].sort_values(by="Medal", ascending=False)
    
    if subplot:
        return go.Bar(
        x=df_dist_["NOC"],
        y=df_dist_["Medal"],
        name=sport,
        marker=dict(
                color=[
                    country_colors.get(country, "#000000") for country in df_dist_["NOC"]
                ]
            ),
        )
    else:
        return px.bar(df_dist_, x="NOC", y="Medal", color="NOC",color_discrete_map=country_colors, labels={"Medal": "Medals"}, title=f"Medal distribution in {sport}")
    
        

def subplot_medal_distribution(df, sport1, sport2, sport3, sport4):
    fig = make_subplots(rows=2, cols=2, subplot_titles=[sport1, sport2, sport3, sport4])
    fig.add_trace(medal_distribution_by_country(df, sport=sport1, subplot=True), row=1, col=1)
    fig.add_trace(medal_distribution_by_country(df, sport=sport2, subplot=True), row=1, col=2)
    fig.add_trace(medal_distribution_by_country(df, sport=sport3, subplot=True), row=2, col=1)
    fig.add_trace(medal_distribution_by_country(df, sport=sport4, subplot=True), row=2, col=2)
    fig.update_layout(title=f"Medal Distribution by Country for {sport1}, {sport2}, {sport3}, {sport4}", showlegend=False)
    return fig


def norway_medals_per_year(df):
    df_norway_medals = filter_medal_entries(df[df["NOC"] == "NOR"])

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
    )

    return fig


def age_by_gender_by_year(df):
    no_df = df[df["NOC"]=="NOR"]
    fig = px.box(
        no_df,
        x="Year",
        y="Age",
        color="Sex",
        points=False,
        title="Age distribution by gender per year"

    )
    fig.update_layout()
    return fig


# TODO add title to 3rd graph norway page



def gender_distribution(df: pd.DataFrame):
    gender_counts = df["Sex"].value_counts().reset_index()
    gender_counts.columns = ["Sex", "Count"]

    fig = px.bar(
        gender_counts,
        x="Sex",
        y="Count",
        title="Gender Distribution",
        labels={"Sex": "Sex", "Count": "Number of Participants"},
        color="Sex",
    )

    return fig


def gender_distribution_by_games(df: pd.DataFrame):
    dist_by_games = df.groupby("Games")["Sex"].value_counts().reset_index()

    fig = px.histogram(dist_by_games, x="Games", y="count", color='Sex', barmode='group')
    
    fig.update_layout(
        title={"text": "Gender Distribution By Games"},
        yaxis_title="Number of Participants",
        xaxis_title="Games",
        legend_title_text="Sex",
    )

    return fig


def events_per_game(df: pd.DataFrame):
    df = df.drop_duplicates(subset=["Event", "Games"])

    events_per_game = df.groupby("Games")["Event"].value_counts().reset_index()

    fig = px.histogram(events_per_game, x="Games", y="count")
    
    fig.update_layout(
        title={"text": "Events Per Game"},
        yaxis_title="Number of Events",
        xaxis_title="Games"
    )

    return fig


def norwegian_sex_age_distribution(df):
    
    df_age = df.drop_duplicates(subset=["Games", "Hash"])
    df_age["Sex"] = df_age["Sex"].apply(lambda x: "Male" if x == "M" else "Female")

    fig = px.histogram(df_age, x="Age", color="Sex", 
                       barmode="overlay", 
                       title="Ages of Norwegian Olympic athletes",
                       )
    fig.update_traces(marker_line_width=1.5)
    fig.update_yaxes(title_text="Amount")
    
    return fig


def norwegian_participants_sex(df, col="Games"):

    nor_wom = df[df["Sex"] == "F"]
    nor_men = df[df["Sex"] == "M"]
    nor_participants = df.groupby(col)["Hash"].nunique().reset_index(name="All")                        # FYI: "Hash" will give an error in GMT but not Dash due to hashing function not being run here in GM
    nor_participants_men = nor_men.groupby(col)["Hash"].nunique().reset_index(name="Male")              # FYI: "Hash" will give an error in GMT but not Dash due to hashing function not being run here in GM
    nor_participants_wom = nor_wom.groupby(col)["Hash"].nunique().reset_index(name="Female")            # FYI: "Hash" will give an error in GMT but not Dash due to hashing function not being run here in GM
    nor_participants = nor_participants.merge(nor_participants_men, on=col, how="left").fillna(0)
    nor_participants = nor_participants.merge(nor_participants_wom, on=col, how="left").fillna(0)
    nor_participants[["Male", "Female"]] = nor_participants[["Male", "Female"]].astype(int)

    fig = px.bar(nor_participants, x=col, y=["Male", "Female"],
                title="Norwegian athletes in the Olympics",
                labels={"value": "Participants", "variable": "Sex", "Games": ""})
    fig.update_xaxes(tickangle=-90)

    return fig


def norwegian_medals_sport_per_games(df, col="Games"):

    nor_medals_sport = df.copy()
    nor_medals_sport = nor_medals_sport.drop_duplicates(subset=["Event", "Games", "Team", "Medal"])
    nor_medals_sport = nor_medals_sport.groupby([col, "Sport"])["Medal"].count().unstack(fill_value=0)
    nor_medals_sport = nor_medals_sport.reset_index()

    fig = px.bar(nor_medals_sport, x=col, y=nor_medals_sport.columns[1:], 
                title="Norwegian Olympic medals by sport",
                labels={"Total": "Medals", "index": "Sport", "Games": "", "value": "Medals"}, 
                color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_xaxes(tickangle=-90)
    
    return fig


# this can be used to visualise both general medals or by sex if arg df is set to a df w/ only wom/men
def norwegian_medals_by_sport(df, headline="Norwegian Olympic medals by sport"):

    def sports_medals():

        sport_medal = df.copy()
        sport_medal = sport_medal.drop_duplicates(subset=["Event", "Games", "Team", "Medal"])
        sport_medal = sport_medal.groupby(["Sport", "Medal"]).size().unstack(fill_value=0)
        sport_medal["Total"] = sport_medal.sum(axis=1)
        sport_medal = sport_medal.reindex(columns=["Bronze", "Silver", "Gold", "Total"])
        sport_medal = sport_medal.sort_values(by="Total", ascending=False)
        sport_medal = sport_medal.reset_index()
        
        return sport_medal
    

    nor_sports_medals = sports_medals()

    fig = px.bar(nor_sports_medals.head(10), x="Sport", y="Total", title=headline, labels={"Total": "Medals", "Sport": ""}, color="Sport")
    fig.update_xaxes(tickangle=-90)
    
    return fig


def norwegian_medals_decade(df):

    def group_and_sort(df, group_by):
        return group_medals(df, group_by).sort_values(by=group_by).reset_index()[["Games", "Total"]]

    nor_wom = df[df["Sex"] == "F"]
    nor_men = df[df["Sex"] == "M"]
    
    nor_medals_all = group_and_sort(df, "Games")
    nor_medals_men = group_and_sort(nor_men, "Games")
    nor_medals_wom = group_and_sort(nor_wom, "Games")
    
    nor_medals_decade = nor_medals_all.merge(nor_medals_men, on="Games", how="left", suffixes=("", "_Male"))
    nor_medals_decade = nor_medals_decade.merge(nor_medals_wom, on="Games", how="left", suffixes=("", "_Female")).fillna(0)
    
    nor_medals_decade = nor_medals_decade.rename(columns={"Total": "Medals", "Total_Male": "Male", "Total_Female": "Female"})
    nor_medals_decade["Decade"] = nor_medals_decade["Games"].apply(lambda row: int(row[:3] + "0"))
    nor_medals_decade = nor_medals_decade.groupby("Decade", as_index=False)[["Medals", "Male", "Female"]].sum()

    # the below code originally came from Copilot with the prompt: "Using plotly express and pandas, how can I plot multiple pie plots with subplots from row values of a dataframe?"
    num_rows = 2
    num_cols = 6
    
    fig = make_subplots(rows=num_rows, cols=num_cols,
                        specs=[[{"type": "domain"}] * num_cols] * num_rows,
                        subplot_titles=[f"{decade}s" for decade in nor_medals_decade["Decade"]])
    
    for i, row in nor_medals_decade.iterrows():
        row_idx = (i // num_cols) + 1
        col_idx = (i % num_cols) + 1
        
        fig.add_trace(go.Pie(labels=["Male", "Female"],
                             values=[row["Male"], row["Female"]],
                             name=f"{row["Decade"]}s",
                             textposition="inside",
                             textinfo="percent",
                             insidetextorientation="horizontal"),
                             row=row_idx, col=col_idx)
    
    fig.update_layout(title_text="Medals won by Norwegian male and female athletes per decade",
                      height=300 * num_rows, showlegend=True, uniformtext=dict(minsize=10, mode="hide"))
    # the above code originally came from Copilot with the prompt: "Using plotly express and pandas, how can I plot multiple pie plots with subplots from row values of a dataframe?"
    
    return fig
 

def medal_coloured_bars(df, col="Games", top=False):

    df_medal_count = group_medals(df, col).sort_values(by=col)
    df_medal_count = df_medal_count.reset_index()

    if top == True:
        df_medal_count = df_medal_count.sort_values(by="Total", ascending=False)
        df_medal_count = df_medal_count.head(20)

    fig = px.bar(df_medal_count, x=col, 
                 y=["Bronze", "Silver", "Gold"],
                 title="Olympic medals",
                 labels={"Total": "Medals", "index": "Sport", "Games": "", "value": "Medals", "variable": ""}, 
                 color_discrete_sequence=["peru", "silver", "gold"])
    fig.update_xaxes(tickangle=-90)

    return fig


def norwegian_medals_season(df):

    nor_medals_winter = df[df["Season"] == "Winter"].dropna(subset=["Medal"]).drop_duplicates(subset=["Event", "Games", "Team", "Medal"])
    nor_medals_summer = df[df["Season"] == "Summer"].dropna(subset=["Medal"]).drop_duplicates(subset=["Event", "Games", "Team", "Medal"])
    medals_winter = nor_medals_winter.groupby("Games")["Medal"].count().reset_index(name="Medals")
    medals_summer = nor_medals_summer.groupby("Games")["Medal"].count().reset_index(name="Medals")

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Winter games", "Summer games"))
    fig.add_trace(go.Bar(x=medals_winter["Games"], y=medals_winter["Medals"], marker_color="skyblue"), row=1, col=1)
    fig.add_trace(go.Bar(x=medals_summer["Games"], y=medals_summer["Medals"], marker_color="orange"), row=1, col=2)
    fig.update_layout(title_text="Norwegian seasonal medals", showlegend=False, yaxis_title="Medals")
    fig.update_yaxes(range=[0, 35]) 
    fig.update_xaxes(tickangle=-90)
    
    return fig


def top_medals_winter(df):
    winter_medals = df[df["Season"] == "Winter"].dropna(subset=["Medal"])
    winter_medals = winter_medals.drop_duplicates(subset=["Event", "Games", "Team", "Medal"])
    winter_medals = winter_medals.groupby("NOC")["Medal"].count().reset_index(name="Medals")
    winter_medals = winter_medals.sort_values(by="Medals", ascending=False)

    fig = px.bar(winter_medals.head(10), x="NOC", y="Medals", title="Olympic winter game medals by country", labels={"NOC": ""}, color="NOC")       # TODO: add country colour map (didn't work with the global variable)
    fig.update_layout(showlegend=False)
    
    return fig


def medals_by_sport_and_sex(df, headline):

    def sports_medals(df, group_by):

        sport_medal = df.drop_duplicates(subset=["Event", "Games", "Team", "Medal"])
        sport_medal = sport_medal.groupby([group_by, "Medal"]).size().unstack(fill_value=0)
        sport_medal["Total"] = sport_medal.sum(axis=1)
        sport_medal = sport_medal.reindex(columns=["Bronze", "Silver", "Gold", "Total"])
        sport_medal = sport_medal.sort_values(by="Total", ascending=False)
        sport_medal = sport_medal.reset_index()
        
        return sport_medal
    
    wom = df[df["Sex"] == "F"]
    men = df[df["Sex"] == "M"]

    sports_medals_all = sports_medals(df, group_by="Sport")
    sports_medals_men = sports_medals(men, group_by="Sport")
    sports_medals_wom = sports_medals(wom, group_by="Sport")

    sports_list = sports_medals_all["Sport"].tolist()
    color_map = {sport: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, sport in enumerate(sports_list)}     # code from Copilot with the prompt: "Each value in sports_list should have a consistent colour when plotted"

    fig = make_subplots(rows=2, cols=2, subplot_titles=("Overall", "Male", "Female"), specs=[[{"colspan": 2}, None], [{}, {}]])
    fig.add_trace(go.Bar(x=sports_medals_all["Sport"].head(20), y=sports_medals_all["Total"], name="Overall", marker_color=[color_map[sport] for sport in sports_medals_all["Sport"]]), row=1, col=1)
    fig.add_trace(go.Bar(x=sports_medals_men["Sport"].head(10), y=sports_medals_men["Total"], name="Male", marker_color=[color_map[sport] for sport in sports_medals_men["Sport"]]), row=2, col=1)
    fig.add_trace(go.Bar(x=sports_medals_wom["Sport"].head(10), y=sports_medals_wom["Total"], name="Female", marker_color=[color_map[sport] for sport in sports_medals_wom["Sport"]]), row=2, col=2)
    fig.update_layout(title_text=headline, showlegend=False, height=800)
    fig.update_yaxes(title_text="Medals")
    fig.update_xaxes(tickangle=-90)

    return fig


