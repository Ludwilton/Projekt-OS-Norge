import plotly_express as px
from data_utils import group_medals, get_NOC_color, round_down_to_nearest_ten, round_up_to_nearest_ten
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# This setting is used to avoid a Pandas FutureWarning (SettingWithCopyWarning)
pd.options.mode.copy_on_write = True

country_colors = get_NOC_color()


def most_medals_by_country(df: pd.DataFrame):
    medal_counts = group_medals(df, "NOC")
    medal_counts = medal_counts[medal_counts["Total"] > 0]
    medal_counts = medal_counts.sort_values(by="Total", ascending=False)
    medal_counts = medal_counts.iloc[:20]

    return px.bar(
        medal_counts, 
        x=medal_counts.index, 
        y=medal_counts["Total"], 
        title="Countries with most amount of medals", 
        color=medal_counts.index, 
        color_discrete_sequence=px.colors.qualitative.Light24,
        labels={"y": "Number of Medals"}
    )


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


def age_distribution_by_sports(df: pd.DataFrame, sports = ["Gymnastics","Shooting","Football","Alpine Skiing"]):
    df_filt = df.drop_duplicates(subset=["Sport", "Games", "ID"])
    df_filt = df_filt.dropna(subset=["Age"])
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


def medal_distribution_by_country(df: pd.DataFrame, sport="Alpine Skiing", subplot=False):
    df_all_unique_participants = df.drop_duplicates(subset=["ID"])

    # Group the data and count medals for each sport and country. Ignore rows without medals.
    medals_by_country = df_all_unique_participants.groupby(["NOC", "Sport"])["Medal"].count().reset_index()
    all_medals_df = medals_by_country[medals_by_country["Medal"] > 0]
    
    df_dist = all_medals_df[all_medals_df["Sport"]==sport].sort_values(by="Medal", ascending=False)
    
    if subplot:
        return go.Bar(
        x=df_dist["NOC"],
        y=df_dist["Medal"],
        name=sport,
        marker=dict(
                color=[
                    country_colors.get(country, "#000000") for country in df_dist["NOC"]
                ]
            ),
        )
    else:
        return px.bar(
            df_dist, 
            x="NOC", 
            y="Medal", 
            color="NOC",
            color_discrete_map=country_colors, 
            labels={"Medal": "Medals"}, 
            title=f"Medal distribution in {sport}"
        )


def subplot_medal_distribution(df: pd.DataFrame, sport1, sport2, sport3, sport4):
    fig = make_subplots(rows=2, cols=2, subplot_titles=[sport1, sport2, sport3, sport4])
    fig.add_trace(medal_distribution_by_country(df, sport=sport1, subplot=True), row=1, col=1)
    fig.add_trace(medal_distribution_by_country(df, sport=sport2, subplot=True), row=1, col=2)
    fig.add_trace(medal_distribution_by_country(df, sport=sport3, subplot=True), row=2, col=1)
    fig.add_trace(medal_distribution_by_country(df, sport=sport4, subplot=True), row=2, col=2)
    fig.update_layout(title=f"Medal Distribution by Country for {sport1}, {sport2}, {sport3}, {sport4}", showlegend=False)
    return fig


def age_by_gender_by_year(df: pd.DataFrame):
    plot_df = df.copy()
    plot_df["Sex"] = plot_df["Sex"].apply(lambda x: "Male" if x == "M" else "Female")

    fig = px.box(
        plot_df,
        x="Year",
        y="Age",
        color="Sex",
        points=False,
        title="Age distribution by gender per year",
        labels={"Sex": ""}
    )
    fig.update_layout()

    return fig


def norwegian_sex_age_distribution(df: pd.DataFrame):
    df_age = df.drop_duplicates(subset=["Games", "Hash"])
    df_age["Sex"] = df_age["Sex"].apply(lambda x: "Male" if x == "M" else "Female")

    fig = px.histogram(
        df_age,
        x="Age",
        color="Sex", 
        barmode="overlay", 
        title="Ages of Norwegian Olympic athletes",
        labels={"Sex": ""}
    )

    fig.update_traces(marker_line_width=1.5)
    fig.update_yaxes(title_text="Amount")
    
    return fig


def norwegian_participants_sex(df: pd.DataFrame, col="Games"):
    nor_wom = df[df["Sex"] == "F"]
    nor_men = df[df["Sex"] == "M"]

    # Count the unique number of participants
    nor_participants = df.groupby(col)["ID"].nunique().reset_index(name="All")
    nor_participants_men = nor_men.groupby(col)["ID"].nunique().reset_index(name="Male")
    nor_participants_wom = nor_wom.groupby(col)["ID"].nunique().reset_index(name="Female")
    
    # Merge to one DataFrame where amount of Male and Female are stored in seperate columns
    nor_participants = nor_participants.merge(nor_participants_men, on=col, how="left").fillna(0)
    nor_participants = nor_participants.merge(nor_participants_wom, on=col, how="left").fillna(0)
    nor_participants[["Male", "Female"]] = nor_participants[["Male", "Female"]].astype(int)

    fig = px.bar(
        nor_participants, 
        x=col, 
        y=["Male", "Female"],
        title="Norwegian athletes in the Olympics",
        labels={"value": "Participants", "variable": "", "Games": ""}
    )

    fig.update_xaxes(tickangle=-90)

    return fig


def norwegian_medals_decade(df: pd.DataFrame):

    def group_and_sort(df: pd.DataFrame, group_by):
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
    
    fig = make_subplots(
        rows=num_rows, 
        cols=num_cols,
        specs=[[{"type": "domain"}] * num_cols] * num_rows,
        subplot_titles=[f"{decade}s" for decade in nor_medals_decade["Decade"]]
    )
    
    for i, row in nor_medals_decade.iterrows():
        row_idx = (i // num_cols) + 1
        col_idx = (i % num_cols) + 1
        
        fig.add_trace(
            go.Pie(
                labels=["Male", "Female"],
                values=[row["Male"], row["Female"]],
                name=f"{row["Decade"]}s",
                textposition="inside",
                textinfo="percent",
                insidetextorientation="horizontal"
            ),
            row=row_idx, col=col_idx
        )
    
    fig.update_layout(
        title_text="Medals won by Norwegian male and female athletes per decade",
        height=300 * num_rows, 
        showlegend=True, 
        uniformtext=dict(minsize=10, mode="hide")
    )
    # the above code originally came from Copilot with the prompt: "Using plotly express and pandas, how can I plot multiple pie plots with subplots from row values of a dataframe?"
    
    return fig
 

def medal_coloured_bars(df: pd.DataFrame, col="Games", top=False):
    df_medal_count = group_medals(df, col).sort_values(by=col)
    df_medal_count = df_medal_count.reset_index()

    if top == True:
        df_medal_count = df_medal_count.sort_values(by="Total", ascending=False)
        df_medal_count = df_medal_count.head(20)

    fig = px.bar(
        df_medal_count, 
        x=col, 
        y=["Bronze", "Silver", "Gold"],
        title="Olympic medals",
        labels={"Total": "Medals", "index": "Sport", "Games": "", "value": "Medals", "variable": ""}, 
        color_discrete_sequence=["peru", "silver", "gold"]
    )
    fig.update_xaxes(tickangle=-90)

    return fig


def norwegian_medals_season(df: pd.DataFrame):
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


def top_medals_winter(df: pd.DataFrame):
    winter_medals = df[df["Season"] == "Winter"].dropna(subset=["Medal"])
    winter_medals = winter_medals.drop_duplicates(subset=["Event", "Games", "Team", "Medal"])
    winter_medals = winter_medals.groupby("NOC")["Medal"].count().reset_index(name="Medals")
    winter_medals = winter_medals.sort_values(by="Medals", ascending=False)

    fig = px.bar(
        winter_medals.head(10), 
        x="NOC", 
        y="Medals", 
        title="Olympic winter game medals by country", 
        labels={"NOC": ""}, 
        color="NOC"
    )
    fig.update_layout(showlegend=False)
    
    return fig


def medals_by_sport_and_sex(df: pd.DataFrame, headline):

    def sports_medals(df: pd.DataFrame, group_by):
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


def height_and_weight_correlation_sport_filter(df: pd.DataFrame, sport):
    df_filt = df.drop_duplicates(subset=["Sport", "Games", "ID"])
    df_filt = df_filt[df_filt["Sport"] == sport]
    gender_colors = {"M": "blue", "F": "red"}

    fig = go.Scatter(
        x=df_filt["Weight"],
        y=df_filt["Height"],
        mode="markers",
        marker=dict(color=df_filt["Sex"].map(gender_colors)),
        name=sport,
    )

    return fig


def subplot_weight_height_correlation(df: pd.DataFrame, sports):
    sport1, sport2, sport3, sport4 = sports
    fig = make_subplots(rows=2, cols=2, subplot_titles=[sport1, sport2, sport3, sport4])

    fig.add_trace(height_and_weight_correlation_sport_filter(df, sport=sport1), row=1, col=1)
    fig.add_trace(height_and_weight_correlation_sport_filter(df, sport=sport2), row=1, col=2)
    fig.add_trace(height_and_weight_correlation_sport_filter(df, sport=sport3), row=2, col=1)
    fig.add_trace(height_and_weight_correlation_sport_filter(df, sport=sport4), row=2, col=2)

    fig.update_xaxes(title_text="Weight (kg)", range=[20, 150])
    fig.update_yaxes(title_text="Height (cm)", range=[120, 220])
    fig.update_layout(title=f"Weight and Height Correlation for {sport1}, {sport2}, {sport3}, {sport4}",height=800, showlegend=False)
    
    return fig


def weight_distribution_by_sports(df: pd.DataFrame, sports = ["Gymnastics","Shooting","Football","Alpine Skiing"]):
    df = df.dropna(subset=["Weight"])

    df_filt = df.drop_duplicates(subset=["Sport", "Games", "ID"])
    df_filt = df_filt[df_filt["Sport"].isin(sports)]

    fig = px.box(
        df_filt,
        x="Sport",
        y="Weight",
        title="Weight distribution by sports",
        color="Sport"
    )
    fig.update_layout(showlegend = False)
    
    return fig


def height_distribution_by_sports(df: pd.DataFrame, sports = ["Gymnastics","Shooting","Football","Alpine Skiing"]):
    df = df.dropna(subset=["Height"])

    df_filt = df.drop_duplicates(subset=["Sport", "Games", "ID"])
    df_filt = df_filt[df_filt["Sport"].isin(sports)]

    fig = px.box(
        df_filt,
        x="Sport",
        y="Height",
        title="Height distribution by sports",
        color="Sport"
    )
    fig.update_layout(showlegend = False)
    
    return fig


def bmi_distribution_by_sports(df: pd.DataFrame, sports=["Gymnastics", "Shooting", "Football", "Alpine Skiing"]):
    df = df.dropna(subset=["Height", "Weight"])

    df["BMI"] = df["Weight"] / (df["Height"] / 100) ** 2

    df_filt = df.drop_duplicates(subset=["Sport", "Games", "ID"])
    df_filt = df_filt[df_filt["Sport"].isin(sports)]

    fig = px.box(
        df_filt,
        x="Sport",
        y="BMI",
        title="BMI distribution by sports",
        color="Sport"
    )
    fig.update_layout(showlegend=False)

    return fig


def bmi_distribution_by_sports_medalists(df: pd.DataFrame, sports=["Gymnastics", "Shooting", "Football", "Alpine Skiing"]):
    df = df.dropna(subset=["Height", "Weight"])

    df["BMI"] = df["Weight"] / (df["Height"] / 100) ** 2

    df_filt = df.drop_duplicates(subset=["Sport", "Games", "ID"])
    df_filt = df_filt[df_filt["Sport"].isin(sports)]
    df_filt = df_filt[df_filt["Medal"].notna()]

    fig = px.box(
        df_filt,
        x="Sport",
        y="BMI",
        title="BMI distribution by sports for medalists",
        color="Sport",
        category_orders={"Sport": sports}
    )
    fig.update_layout(showlegend=False)
    fig.update_yaxes(range=[11,48])

    return fig


def sport_subplots(df: pd.DataFrame, sport):
    df_sport = df[df["Sport"] == sport]
    gender_colors = {"M": "blue", "F": "red"}

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            "Top Medal-Winning Countries", "Age Distribution",
            "Gender Distribution", "Body Metrics of Athletes",
        ]
    )

    def countries_with_most_medals_in_sport():
        # Group medals by country
        medal_counts = group_medals(df_sport)

        # Filter to only get countries with medals (Total > 0),
        # sort by total of medals, and get the top 20 countries with most medals.
        medal_counts = medal_counts[medal_counts["Total"] > 0].sort_values(
            by="Total", ascending=False
        ).iloc[:20]

        return go.Bar(
            x=medal_counts.index,
            y=medal_counts["Total"],
            name="Medals",
            marker=dict(
                color=[
                    country_colors.get(NOC, "#000000")
                    for NOC in medal_counts.index
                ]
            ),
        )

    def age_distribution_by_gender():
        traces = []

        # Loop through each gender and create a histogram to visualize the age distribution for both genders.
        for gender, color in gender_colors.items():
            df_gender = df_sport[df_sport["Sex"] == gender]

            # Every histogram is added to the traces-list
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
        # Ensures that "gender_counts" always includes the indexes "M" and "F", even if either is missing in df_sport["Sex"].
        # Uses fill_value=0 to set the value to 0 for missing data.
        gender_counts = df_sport["Sex"].value_counts().reindex(["M", "F"], fill_value=0)

        return go.Bar(
            x=["Male", "Female"],
            y=gender_counts.values,
            marker_color=df_sport["Sex"].map(gender_colors),
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


    # Row 1, Col 1
    fig.add_trace(countries_with_most_medals_in_sport(), row=1, col=1)

    # Row 1, Col 2
    for trace in age_distribution_by_gender():
        fig.add_trace(trace, row=1, col=2)

    # Row 2, Col 1
    fig.add_trace(gender_distribution_of_sport(), row=2, col=1)

    # Row 2, Col 2
    fig.add_trace(height_and_weight_correlation(), row=2, col=2)


    fig.update_xaxes(title_text="Country (NOC)", row=1, col=1)
    fig.update_yaxes(title_text="Number of Medals", row=1, col=1)

    fig.update_xaxes(title_text="Age", range=[round_down_to_nearest_ten(df["Age"].min()), round_up_to_nearest_ten(df["Age"].max())], row=1, col=2)
    fig.update_yaxes(title_text="Number of Participants", row=1, col=2)

    fig.update_xaxes(title_text="Gender", row=2, col=1)
    fig.update_yaxes(title_text="Number of Participants", row=2, col=1)

    fig.update_xaxes(title_text="Weight (kg)", range=[round_down_to_nearest_ten(df["Weight"].min()), round_up_to_nearest_ten(df["Weight"].max())], row=2, col=2)
    fig.update_yaxes(title_text="Height (cm)", range=[round_down_to_nearest_ten(df["Height"].min()), round_up_to_nearest_ten(df["Height"].max())], row=2, col=2)

    fig.update_layout(
        title=f"Statistics for {sport}",
        showlegend=False,
        height=800,
        margin=dict(l=50, r=50, t=100, b=50),
    )

    return fig
