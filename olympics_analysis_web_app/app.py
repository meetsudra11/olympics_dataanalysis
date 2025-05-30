import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import preprocessor,helper
from helper import medal_tally
import plotly.express as px

from preprocessor import athlete_df

# olympics main data
df = preprocessor.preprocess()

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
    country_df = helper.yearwise_country_medaltally(df, 'USA')
    fig = px.line(country_df, x='Year', y='Medal')
    st.title("Medal Tally for Countries over the years")
    st.plotly_chart(fig)


