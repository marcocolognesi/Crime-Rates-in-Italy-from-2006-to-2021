# Libraries
import pandas as pd
import numpy as np
import json
import streamlit as st
import plotly.express as px

# Importing 'final.csv' created in the data manipulation notebook
df = pd.read_csv("data/final.csv")

# Importing JSON file created in the data manipulation notebook
prov_json = json.load(open('data\shapefiles\province.geojson', 'r'))

# Initial page configuration settings
st.set_page_config(layout='wide')
st.title('Trend of Crime Rates in Italy from 2006 to 2021')
st.write("## Overview of the Incidence of the Rates over 100.000 Population around the Italian territory")

# Adding a selection box to choose a crime type
crime_option = st.selectbox('Select the crime type:', (list(df['Crime'].unique())))
# Filtering the df with the crime type chosen in the selection box
df_crime_option = df.loc[df['Crime'] == crime_option]

# Adding a selection box to choose the year 
year_option = st.selectbox('Select the year:', (list(df['Year'].unique())))
# Filtering the df with the crime type chosen in the selection box and the year
df_crime_option_and_year = df_crime_option.loc[df_crime_option['Year'] == year_option]

# Reset index & dropping useless columns
df_crime_option_and_year = df_crime_option_and_year.reset_index()
df_crime_option_and_year = df_crime_option_and_year.drop(columns=['index', 'Unnamed: 0'])

# Creating choropleth map with plotly
fig = px.choropleth(data_frame = df_crime_option_and_year,
                    geojson = prov_json, 
                    locations = df_crime_option_and_year['Province'],
                    featureidkey = 'properties.DEN_UTS',
                    color = df_crime_option_and_year['Value over 100000 population'],
                    color_continuous_scale="Reds",
                    hover_data=['Population', 'Value'],
                    projection= 'mercator')
# Centering the map
fig.update_geos(fitbounds='locations', visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# Changing background color
fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

# Showing map
st.plotly_chart(fig,theme='streamlit', use_container_width=True)


# Manipulation to display the dataframe
# Sorting by the rates over 100.000 population
df_crime_option_and_year_sorted = df_crime_option_and_year.sort_values(by=['Value over 100000 population'], ascending = False)
# Adding rank columns
df_crime_option_and_year_sorted['Rank'] = df_crime_option_and_year_sorted['Value over 100000 population'].rank(ascending = False)
# Setting 'Rank' column as index
df_crime_option_and_year_sorted = df_crime_option_and_year_sorted.set_index('Rank')
# Dropping useless columns
df_crime_option_and_year_sorted = df_crime_option_and_year_sorted.drop(columns = ['Crime', 'Year'])

# Showing the dataframe
st.dataframe(df_crime_option_and_year_sorted, use_container_width= True)