import streamlit as st
import pandas as pd
import preprocessor,helper

df = preprocessor.preprocess()

user_menu = st.sidebar.radio(
    'Select an Option', ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)
st.dataframe(df)

if user_menu == 'Medal Tally':
    st.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.medal_tally(df)
    st.dataframe(medal_tally)