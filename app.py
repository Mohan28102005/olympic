import streamlit as st
import pandas as pd
import plotly.express as px
import helper
import seaborn as sns
import preprocessor
import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff
df=pd.read_csv("athlete_events.csv")
region_df=pd.read_csv("noc_regions.csv")
st.sidebar.image("olympics.png")
user_menu=st.sidebar.radio(
    'Select an option',
    ["Medal Tally","Overall Analysis","Country-wise Analysis","Athlete wise Analysis"]
)
st.title("Olympic analysis")
df=preprocessor.preprocess(df,region_df)
if user_menu=="Medal Tally":
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Country",country)
    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    # medal_tally=medal_tally.head(10)
    st.table(medal_tally)
if user_menu=="Overall Analysis":
    st.title("Overall Analysis")
    editions=df["Year"].unique().shape[0]-1
    cities=df["City"].unique().shape[0]
    sports=df["Sport"].unique().shape[0]
    events=df["Event"].unique().shape[0]
    athletes=df["Name"].unique().shape[0]
    nations=df["region"].unique().shape[0]
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)
    nations_over_time=helper.participating_nations_over_time(df)
    nations_over_time.columns = ["Year", "No of countries"]
    fig = px.line(nations_over_time, x="Year", y="No of countries")
    st.title("Participating Years over the years")
    st.plotly_chart(fig)
    st.title("Number of Events over the years")
    events_over_time=helper.events_over_years(df)
    fig1= px.line(events_over_time, x="Year", y="No of Events")
    st.plotly_chart(fig1)
    st.title("Number of Athletes participating over time")
    athletes_over_time=helper.athletes_over_time(df)
    fig2=px.line(athletes_over_time, x="Year", y="No of Athletes")
    st.plotly_chart(fig2)
    st.title("Number of Events over time(Each Sport)")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    ax=sns.heatmap(x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype("int"),annot=True)
    st.pyplot(fig)
    st.title("Most successful Athletes")
    sports_list=df["Sport"].unique().tolist()
    sports_list=sorted(sports_list)
    sports_list.insert(0,"Overall")
    selected_sport=st.selectbox("Select a sport",sports_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=="Country-wise Analysis":
    st.title("Country Wise Analysis")
    country_list=df["region"].unique().tolist()
    country = np.unique(df["region"].dropna().values).tolist()
    country.sort()
    selected_country=st.selectbox("Select Country",country)
    country_df=helper.yearwise_medal_tally(df,selected_country)
    fig=px.line(country_df,x="Year",y="Medal")
    st.title(selected_country+" Medal Tally over the years")
    st.plotly_chart(fig)
    st.title("Top 10 Athletes of "+selected_country)
    temp_df = df.dropna(subset=["Medal"])
    temp_df = temp_df[temp_df["region"] == selected_country]
    athlete_medal_counts = temp_df["Name"].value_counts().head(10).reset_index()
    athlete_medal_counts.columns = ["Name", "Total Medals"]
    st.table(athlete_medal_counts)
if user_menu=="Athlete wise Analysis":
    st.title("Age Distribution")
    x1,x2,x3,x4=helper.age_wise_analysis(df)
    fig = ff.create_distplot([x1, x2, x3, x4], ["Gold Medalist", "Silver Medalist", "Bronze Medalist", "Overall Age"],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=100,height=600)
    st.plotly_chart(fig)
    all_sports=helper.get_all_sports(df)
    st.title("Height Vs Weight")
    selected_sport=st.selectbox("Select a sport",all_sports)
    temp_df=helper.height_weight_distribution(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x="Weight", y="Height", hue="Medal", data=temp_df)
    st.pyplot(fig)
    st.title("Men Vs Women Participation over the Years")
    athlete_df = df.drop_duplicates(subset=["Name", "region"])
    athlete_df["Medal"].fillna("No Medal", inplace=True)
    men_df = athlete_df[athlete_df["Sex"] == "M"].groupby("Year").count()["Name"].reset_index()
    women_df = athlete_df[athlete_df["Sex"] == "F"].groupby("Year").count()["Name"].reset_index()
    final = men_df.merge(women_df, on="Year")
    final.rename(columns={"Name_x": "Male", "Name_y": "Female"}, inplace=True)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig)