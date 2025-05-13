import numpy as np
def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    medal_tally=medal_tally.groupby("region").sum()[["Gold","Silver","Bronze"]].sort_values("Gold",ascending=False).reset_index()
    medal_tally["total"]=medal_tally["Gold"]+medal_tally["Silver"]+medal_tally["Bronze"]
    medal_tally["Gold"]=medal_tally["Gold"].astype("int")
    medal_tally["Silver"] = medal_tally["Silver"].astype("int")
    medal_tally["Bronze"] = medal_tally["Bronze"].astype("int")
    return medal_tally

def country_year_list(df):
    years=set(df["Year"])
    years=sorted(years)
    years.insert(0,"Overall")
    country=np.unique(df["region"].dropna().values).tolist()
    country.sort()
    country.insert(0,"Overall")
    return years,country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    for medal in ["Gold", "Silver", "Bronze"]:
        medal_df[medal] = medal_df[medal].fillna(0).astype(int)

    flag = 0
    if year == "Overall" and country == "Overall":
        temp_df = medal_df
    elif year != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df["Year"] == int(year)]
    elif year == "Overall" and country != "Overall":
        flag = 1
        temp_df = medal_df[medal_df["region"] == country]
    else:
        temp_df = medal_df[(medal_df["Year"] == int(year)) & (medal_df["region"] == country)]

    if flag == 1:
        x = temp_df.groupby("Year").sum(numeric_only=True)[["Gold", "Silver", "Bronze"]].sort_values(
            "Year").reset_index()
    else:
        x = temp_df.groupby("region").sum(numeric_only=True)[["Gold", "Silver", "Bronze"]].sort_values("Gold",ascending=False).reset_index()

    x["total"] = x["Gold"] + x["Silver"] + x["Bronze"]
    return x

def participating_nations_over_time(df):
    nations_over_time = df.drop_duplicates(["Year", "region"])["Year"].value_counts().reset_index()
    nations_over_time = nations_over_time.sort_values("Year")
    return nations_over_time
def events_over_years(df):
    events_over_time = df.drop_duplicates(["Year", "Event"])["Year"].value_counts().reset_index()
    events_over_time = events_over_time.sort_values("Year")
    events_over_time.columns = ["Year", "No of Events"]
    return events_over_time
def athletes_over_time(df):
    athletes_over_time = df.drop_duplicates(["Year", "Name"])["Year"].value_counts().reset_index()
    athletes_over_time = athletes_over_time.sort_values("Year")
    athletes_over_time.columns = ["Year", "No of Athletes"]
    return athletes_over_time

def most_successful(df,sport):
  temp_df=df.dropna(subset=["Medal"])
  if sport!= "Overall":
    temp_df=temp_df[temp_df["Sport"]==sport]
  x=temp_df["Name"].value_counts().head(10).reset_index()
  x.columns=["Name","Medals"]
  x=x.merge(df,left_on="Name",right_on="Name",how="left")[["Name","Medals","region"]].drop_duplicates()
  return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"], inplace=True)
    new_df = temp_df[temp_df["region"] == country]
    final_df = new_df.groupby("Year")["Medal"].count().reset_index()
    return final_df
def age_wise_analysis(df):
    athlete_df = df.drop_duplicates(subset=["Name", "region"])
    x1 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()
    x4 = athlete_df["Age"].dropna()
    return x1,x2,x3,x4
def height_weight_distribution(df,selected_sport):
    athlete_df = df.drop_duplicates(subset=["Name", "region"])
    athlete_df["Medal"].fillna("No Medal", inplace=True)
    temp_df = athlete_df[athlete_df["Sport"] == selected_sport]
    return temp_df
def get_all_sports(df):
    sports=df["Sport"].tolist()
    sports = set(sports)
    sports=sorted(sports)
    return sports