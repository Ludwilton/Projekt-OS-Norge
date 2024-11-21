import plotly_express as px
from data_utils import group_medals, filter_medal_entries
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

countries = [ # byt till : "df["NOC"].unique()"
    "CHN", "DEN", "NED", "USA", "FIN", "NOR", "ROU", "EST", "FRA", "MAR",
    "ESP", "EGY", "IRI", "BUL", "ITA", "CHA", "AZE", "SUD", "RUS", "ARG",
    "CUB", "BLR", "GRE", "CMR", "TUR", "CHI", "MEX", "URS", "NCA", "HUN",
    "NGR", "ALG", "KUW", "BRN", "PAK", "IRQ", "UAR", "LIB", "QAT", "MAS",
    "GER", "CAN", "IRL", "AUS", "RSA", "ERI", "TAN", "JOR", "TUN", "LBA",
    "BEL", "DJI", "PLE", "COM", "KAZ", "BRU", "IND", "KSA", "SYR", "MDV",
    "ETH", "UAE", "YAR", "INA", "PHI", "SGP", "UZB", "KGZ", "TJK", "EUN",
    "JPN", "CGO", "SUI", "BRA", "FRG", "GDR", "MON", "ISR", "URU", "SWE",
    "ISV", "SRI", "ARM", "CIV", "KEN", "BEN", "UKR", "GBR", "GHA", "SOM",
    "LAT", "NIG", "MLI", "AFG", "POL", "CRC", "PAN", "GEO", "SLO", "CRO",
    "GUY", "NZL", "POR", "PAR", "ANG", "VEN", "COL", "BAN", "PER", "ESA",
    "PUR", "UGA", "HON", "ECU", "TKM", "MRI", "SEY", "TCH", "LUX", "MTN",
    "CZE", "SKN", "TTO", "DOM", "VIN", "JAM", "LBR", "SUR", "NEP", "MGL",
    "AUT", "PLW", "LTU", "TOG", "NAM", "AHO", "ISL", "ASA", "SAM", "RWA",
    "DMA", "HAI", "MLT", "CYP", "GUI", "BIZ", "YMD", "KOR", "THA", "BER",
    "ANZ", "SCG", "SLE", "PNG", "YEM", "IOA", "OMA", "FIJ", "VAN", "MDA",
    "YUG", "BAH", "GUA", "SRB", "IVB", "MOZ", "CAF", "MAD", "MAL", "BIH",
    "GUM", "CAY", "SVK", "BAR", "GBS", "TLS", "COD", "GAB", "SMR", "LAO",
    "BOT", "ROT", "CAM", "PRK", "SOL", "SEN", "CPV", "CRT", "GEQ", "BOL",
    "SAA", "AND", "ANT", "ZIM", "GRN", "HKG", "LCA", "FSM", "MYA", "MAW",
    "ZAM", "RHO", "TPE", "STP", "MKD", "BOH", "TGA", "LIE", "MNE", "GAM",
    "COK", "ALB", "WIF", "SWZ", "BUR", "NBO", "BDI", "ARU", "NRU", "VNM",
    "VIE", "BHU", "MHL", "KIR", "UNK", "TUV", "NFL", "KOS", "SSD", "LES"
]

# används för konsistent unik färg på varje land
palette = px.colors.qualitative.Light24                                 # gpt
palette_cycle = palette * (len(countries) // len(palette) + 1)          # gpt
country_colors = dict(zip(countries, palette_cycle[:len(countries)]))   # gpt


def norway_age_histogram(df):
    norway_athletes = df[df["NOC"] == "NOR"]
 
    fig = px.histogram(
        norway_athletes, 
        x="Age", 
        color="Sex",
        title="Age distribution by gender"
    )

    fig.update_layout(barmode='overlay')
    fig.update_traces(opacity=0.75, marker_line_width=1.5)

    return fig


def countries_with_most_medals_in_sport(df, sport, subplot=False):
    if subplot:
        df_sport = df
    else:
        df_sport = df[df["Sport"] == sport]


    medal_counts = group_medals(df_sport)

    medal_counts = medal_counts[medal_counts["Total"] > 0]

    # Get top 20 countries by total amount of medals
    medal_counts = medal_counts.sort_values(by="Total", ascending=False)
    medal_counts = medal_counts.iloc[:20]

    if subplot:
        num_colors = len(df["NOC"])
        colors = px.colors.qualitative.Plotly * (num_colors // len(px.colors.qualitative.Plotly) + 1) # gpt
        return go.Bar(
            x=medal_counts.index,
            y=medal_counts["Total"],
            name=sport,
            marker=dict(color=[country_colors.get(country, "#000000") for country in medal_counts.index])
        )
    else:
        fig = px.bar(medal_counts, x=medal_counts.index, y=medal_counts["Total"], title=sport, color=medal_counts.index)

        return fig


def age_distribution_of_one_sport(df, sport, subplot=False):
    # TODO: Male och Female måste alltid ha samma färg oavsett om det är flest Male eller Female

    if subplot:
        df_sport = df
    else:
        df_sport = df[df["Sport"] == sport]

    if subplot: 
        # TODO: Kunna se andel Male och Female i grafen
        trace = go.Histogram(
            x=df_sport["Age"],
            name=sport,
            marker_color=px.colors.qualitative.Plotly[0]
        )
        return trace
    else:
        fig = px.histogram(df_sport, x="Age", color="Sex", barmode="overlay", title="Average age of Norwegian Olympic athletes", labels={"Age": "Age", "Sex": "Gender"})

        fig.update_layout(barmode='overlay')
        fig.update_traces(opacity=0.75, marker_line_width=1.5)
        
        return fig


def round_down_to_nearest_ten(number):
    return math.floor(number / 10) * 10

def round_up_to_nearest_ten(number):
    return math.ceil(number / 10) * 10


def sport_subplots(df, sport):
    df_sport = df[df["Sport"] == sport]

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            "Medal Distribution by Country", "Age Distribution", 
            "Gender Distribution", "Height and Weight Correlation"
        ]
    )

    fig.add_trace(countries_with_most_medals_in_sport(df_sport, sport, subplot=True), row=1, col=1)
    fig.add_trace(age_distribution_of_one_sport(df_sport, sport, subplot=True), row=1, col=2) 
    fig.add_trace(gender_distribution_of_sport_subplot(df, sport), row=2, col=1)
    fig.add_trace(height_and_weight_of_sport(df_sport, sport=sport, subplot=True), row=2, col=2)

    min_height = round_down_to_nearest_ten(df["Height"].min())
    min_weight = round_down_to_nearest_ten(df["Weight"].min())

    max_height = round_up_to_nearest_ten(df["Height"].max())
    max_weight = round_up_to_nearest_ten(df["Weight"].max())

    min_age = round_down_to_nearest_ten(df["Age"].min())
    max_age = round_up_to_nearest_ten(df["Age"].max())

    fig.update_xaxes(range=[min_age, max_age], row=1, col=2)

    fig.update_xaxes(range=[min_weight, max_weight], row=2, col=2)
    fig.update_yaxes(range=[min_height, max_height], row=2, col=2)
    
    fig.update_layout(
        title=f"Statistics for {sport}",
        showlegend=False,
        height=800
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
        num_colors = len(df_dist_["NOC"]) # gpt
        colors = px.colors.qualitative.Plotly * (num_colors // len(px.colors.qualitative.Plotly) + 1) # gpt
        return go.Bar(
        x=df_dist_["NOC"],
        y=df_dist_["Medal"],
        name=sport,
        marker=dict(
                color=[
                    country_colors.get(country, "#000000") for country in df_dist_["NOC"]
                ]  # Use predefined country colors
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


def gender_distribution_of_sport_subplot(df: pd.DataFrame, sport):
    df = df[df["Sport"] == sport]
    
    gender_counts = df["Sex"].value_counts()
    
    standard_order = pd.Series([0, 0], index=["M", "F"])
    gender_counts = standard_order.add(gender_counts, fill_value=0).reset_index()
    gender_counts.columns = ["Sex", "Count"]
    gender_counts = gender_counts.sort_values(by="Sex")

    return go.Bar(
        x=gender_counts["Sex"],
        y=gender_counts["Count"],
        marker_color=["red", "blue"],
        name="Participants",
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


def height_and_weight_of_sport(df: pd.DataFrame, sport = "Football", subplot=True):
    color_map = {"F": "red", "M": "blue"}
    
    colors = df["Sex"].map(color_map)

    return go.Scatter(
        x=df["Weight"],
        y=df["Height"],
        mode="markers",
        marker={"color": colors},
    )


# Anders Norway graphs (below)

def norwegian_gender_age_distribution(df=nor):

    df_age = df.copy()
    df_age = df_age.drop_duplicates(subset=["Games", "Hash"])

    fig = px.histogram(df, x="Age", color="Sex", 
                       barmode="overlay", 
                       title="Ages of Norwegian Olympic Athletes", 
                       labels={"count": "Amount", "Sex": "Gender"},
                       color_discrete_sequence=["forestgreen", "orange"])
    fig.update_traces(marker_line_width=1.5)
    
    return fig


def norwegian_participants_gender(df=nor_athletes, col="Games"):
    fig = px.bar(df, x=col, y=["Women", "Men"], 
                color_discrete_sequence=["orange", "forestgreen"], 
                title="Norwegian athletes in the Olympics", 
                labels={"value": "Participants", "variable": "Gender", "Games": ""})
    fig.update_xaxes(tickangle=-90)

    return fig


def norwegian_medals_sport_per_games(df=nor, col="Games"):

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


# this can be used to visualise both general medals or by gender if arg df is set to a df w/ wom/men
def norwegian_medals_by_sport(df=nor, headline="Norwegian Olympic medals by sport"):

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


def norwegian_medals_decade(df=nor):

	nor_wom = nor[nor["Sex"] == "F"]
	nor_men = nor[nor["Sex"] == "M"]
	nor_medals = group_medals()
	nor_medals_wom = group_medals(nor_wom, "Games").sort_values(by="Games")
	nor_medals_men = group_medals(nor_men, "Games").sort_values(by="Games")

	nor_medals_decade = nor_medals.reset_index()
	temp_men = nor_medals_men.reset_index()
	temp_wom = nor_medals_wom.reset_index()
	nor_medals_decade = nor_medals_decade[["Games", "Total"]]
	temp_men = temp_men[["Games", "Total"]]
	temp_wom = temp_wom[["Games", "Total"]]

	nor_medals_decade = nor_medals_decade.merge(temp_men, on="Games", how="left")
	nor_medals_decade = nor_medals_decade.merge(temp_wom, on="Games", how="left").fillna(0)
	nor_medals_decade["Total"] = nor_medals_decade["Total"].astype(int)
	nor_medals_decade = nor_medals_decade.rename(columns={"Total_x": "Medals", "Total_y": "Men", "Total": "Women"})
	nor_medals_decade["Decade"] = nor_medals_decade["Games"].apply(lambda row: int(row[:3] + "0"))
	nor_medals_decade = nor_medals_decade.groupby("Decade", as_index=False)[["Medals", "Men", "Women"]].sum()

	# the below is the result of a Copilot prompt: "Using plotly express and pandas, how can I plot multiple pie plots with subplots from row values of a dataframe?"
	fig = make_subplots(rows=1, cols=len(nor_medals_decade), specs=[[{"type": "domain"}] * len(nor_medals_decade)],
						subplot_titles=[f"{decade}s" for decade in nor_medals_decade["Decade"]])

	for i, row in nor_medals_decade.iterrows():
		fig.add_trace(go.Pie(labels=["Men", "Women"], values=[row["Men"], row["Women"]], name=f"{row["Decade"]}s",
							marker_colors=["forestgreen", "orange"]), 1, i+1)
	# the above is the result of a Copilot prompt: "Using plotly express and pandas, how can I plot multiple pie plots with subplots from row values of a dataframe?"

	fig.update_layout(title_text="Medals won by male and female athletes per decade")
	
	return fig


def medal_coloured_bars(df=nor, col="Games"):

    df_medal_count = group_medals()
    df_medal_count = df_medal_count.reset_index()

    fig = px.bar(df_medal_count, 
             x=col, y=["Bronze", "Silver", "Gold"], 
             title="Norwegian Olympic medals", 
             labels={"Total": "Medals", "index": "Sport", "Games": "", "value": "Medals", "variable": ""}, 
             color_discrete_sequence=["#cd7f32", "#c0c0c0", "#ffd700"])
    fig.update_xaxes(tickangle=-90)

    return fig


def norwegian_medals_season(df=nor):
    
    nor_medals_winter = df[df["Season"] == "Winter"].dropna(subset=["Medal"]).drop_duplicates(subset=["Event", "Games", "Team", "Medal"])
    nor_medals_summer = df[df["Season"] == "Summer"].dropna(subset=["Medal"]).drop_duplicates(subset=["Event", "Games", "Team", "Medal"])
    medals_winter = nor_medals_winter.groupby("Games")["Medal"].count().reset_index(name="Medals")
    medals_summer = nor_medals_summer.groupby("Games")["Medal"].count().reset_index(name="Medals")

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Winter games", "Summer games"))
    fig.add_trace(go.Bar(x=medals_winter["Games"], y=medals_winter["Medals"], marker_color="skyblue"), row=1, col=1)
    fig.add_trace(go.Bar(x=medals_summer["Games"], y=medals_summer["Medals"], marker_color="orange"), row=1, col=2)
    fig.update_layout(title_text="Norwegian seasonal medals", showlegend=False, yaxis_title="Amount")
    fig.update_yaxes(range=[0, 35])
    fig.update_xaxes(tickangle=-90)
    
    return fig


def top_medals_winter():
    winter_medals = df[df["Season"] == "Winter"].dropna(subset=["Medal"])
    winter_medals = winter_medals.drop_duplicates(subset=["Event", "Games", "Team", "Medal"])
    winter_medals = winter_medals.groupby("NOC")["Medal"].count().reset_index(name="Medals")
    winter_medals = winter_medals.sort_values(by="Medals", ascending=False)

    fig = px.bar(winter_medals.head(10), x="NOC", y="Medals", title="Olympic winter game medals by country", labels={"NOC": "", "Medals": "Amount"}, color="NOC")
    fig.update_layout(showlegend=False)
    
    return fig


# Anders Norway graphs (above)