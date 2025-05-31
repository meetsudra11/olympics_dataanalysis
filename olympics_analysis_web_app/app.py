import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import preprocessor,helper
from helper import medal_tally
import plotly.express as px
import plotly.figure_factory as ff

from preprocessor import athlete_df

# olympics main data
df = preprocessor.preprocess()


st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg",
)

# Sidebar through which we will provide options on webpage
st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)

# results on opting medal tally from the menu
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'overall' and selected_country == 'overall':
        st.title('Overall Performance of all the countries so far')
    if selected_year != 'overall' and selected_country == 'overall':
        st.title("Medal Tally in " + str(selected_year))
    if selected_year == 'overall' and selected_country != 'overall':
        st.title("Overall performance of country " + selected_country)
    if selected_year != 'overall' and selected_country != 'overall':
        st.title("Medal Tally in " + str(selected_year) + " for country " + selected_country)

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sport = df['Sport'].unique().shape[0]
    event = df['Event'].unique().shape[0]
    name = df['Name'].unique().shape[0]
    region = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sport")
        st.title(sport)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Event")
        st.title(event)
    with col2:
        st.header("Name")
        st.title(name)
    with col3:
        st.header("Region")
        st.title(region)


    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title("Participating Nations Over Time")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title("No. of Events Over Time")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title("No. of Athlete Over Time")
    st.plotly_chart(fig)

    st.title("No of Events per Sport over Time")
    fig, ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes Over Time")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)

    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title("Country wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_country_medaltally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title("Medal Tally for Countries over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " Excels in the following sport")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot = True)
    st.pyplot(fig)

    st.title("Top 10 players of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)


if user_menu == 'Athlete-wise Analysis':

    ath_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = ath_df['Age'].dropna()
    x2 = ath_df[ath_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = ath_df[ath_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = ath_df[ath_df['Medal'] == 'Bronze']['Age'].dropna()

    plt.figure(figsize=(10, 10))
    age_fig = ff.create_distplot([x1, x2, x3, x4],
                                 ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                                 show_hist=False, show_rug=False)
    st.title("Distribution of Age")
    st.plotly_chart(age_fig)

    x = []
    name = []
    famous_sports = [
        'Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
        'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
        'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
        'Water Polo', 'Hockey', 'Rowing', 'Fencing',
        'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
        'Tennis', 'Golf', 'Softball', 'Archery',
        'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
        'Rhythmic Gymnastics', 'Rugby Sevens',
        'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey'
    ]
    for sport in famous_sports:
        temp_df = ath_df[ath_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    sport_fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    st.title("Distribution of Age by Sport")
    st.plotly_chart(sport_fig)

    final = helper.menvswomen(df)
    fig = px.line(final, x='Year', y=["Male", "Female"])
    fig.update_layout(autosize=True, hovermode='x')
    st.plotly_chart(fig)