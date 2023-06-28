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
st.title('Trend of Crime Rates over Italy from 2006 to 2021')
st.write("## An Overview of the Incidence of the Rates over 100.000 Population around the Italian territory")

# Adding a selection box to choose a crime type
crime_option = st.selectbox('Pick one', (list(df['Crime'].unique())))
# Filtering the df with the crime type chosen in the selection box
df_crime_option = df.loc[df['Crime'] == crime_option]

# Creating choropleth map with plotly
fig = px.choropleth(data_frame = df_crime_option,
                    geojson = prov_json, 
                    locations = df_crime_option['Province'],
                    featureidkey = 'properties.DEN_UTS',
                    color = df_crime_option['Value over 100000 population'],
                    color_continuous_scale="Reds",
                    hover_data=['Population', 'Value'],
                    projection= 'mercator',
                    animation_frame = 'Year')
# Centering the map
fig.update_geos(fitbounds='locations', visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# Changing background color
fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

# Showing map
st.plotly_chart(fig,theme='streamlit', use_container_width=True)