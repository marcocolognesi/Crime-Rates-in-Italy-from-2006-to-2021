import pandas as pd
import numpy as np
import json
import streamlit as st
import plotly.express as px
import plotly.io as pio
import functions

# Importing final.csv created in the data manipulation notebook
df = pd.read_csv("data/final.csv")

# Initial page configuration settings
st.set_page_config(layout='wide')
st.title('Trend of Crime Rates over Italy from 2006 to 2021')


# First part --> see the global trend of each type of crime

st.write("## Overall trend of each type of crime")

crime_option = st.selectbox('Choose the type of crime: ',
                            (list(df['Crime'].unique())))

# Creating a DF grouped by Crime and Year and with the values summed through all the areas
df_grouped_by_crime_year = df.groupby(['Crime', 'Year']).sum(numeric_only= True)['Value'].reset_index()
# Filtering the DF with the selected crime
df_grouped_by_crime_selected = df_grouped_by_crime_year.loc[df_grouped_by_crime_year['Crime'] == crime_option]

fig = px.line(data_frame = df_grouped_by_crime_selected,
            x = 'Year',
            y = 'Value',
            color = 'Crime',
            title = f"Overall trend over the years (absolute values)")
st.plotly_chart(fig)

st.write(f"### Macro-area comparison of the '{crime_option}' crime")
# Multiselection box to select the areas to compare
area_multiselection = st.multiselect('Choose the areas you want to compare: ',
                                     (list(df['Area'].unique())))
col1, col2= st.columns(2)
# Plotting second column
with col1:
    df_grouped_by_area_crime_year = df.groupby(['Area', 'Crime', 'Year']).sum(numeric_only=True)['Value'].reset_index()
    df_grouped_by_area_crime_selected = df_grouped_by_area_crime_year.loc[df_grouped_by_area_crime_year['Crime'] == crime_option]
    area_list = df['Area'].unique()
    for area in area_list:
        if area not in area_multiselection:
            df_grouped_by_area_crime_selected = df_grouped_by_area_crime_selected.loc[df_grouped_by_area_crime_selected['Area'] != area]

    fig = px.line(data_frame = df_grouped_by_area_crime_selected,
            x = 'Year',
            y = 'Value',
            color = 'Area',
            title = f"Overall trend in the different areas (absolute values)")
    st.plotly_chart(fig)
# Plotting third column
with col2:
    df_grouped_by_area_crime_year_incidence = df.groupby(['Area', 'Crime', 'Year']).sum(numeric_only=True)['Value over 100000 population'].reset_index()
    df_grouped_by_area_crime_selected_incidence = df_grouped_by_area_crime_year_incidence.loc[df_grouped_by_area_crime_year_incidence['Crime'] == crime_option]
    area_list = df['Area'].unique()
    for area in area_list:
        if area not in area_multiselection:
            df_grouped_by_area_crime_selected_incidence = df_grouped_by_area_crime_selected_incidence.loc[df_grouped_by_area_crime_selected_incidence['Area'] != area]

    fig = px.line(data_frame = df_grouped_by_area_crime_selected_incidence,
            x = 'Year',
            y = 'Value over 100000 population',
            color = 'Area',
            title = f"Overall trend in the different areas (Values over 100000 population)")
    st.plotly_chart(fig)

st.write(f"### Regional comparison of the '{crime_option}' crime")
# Multiselection box to select the regions
region_multiselection = st.multiselect('Choose the regions you want to compare: ',
                                       (list(df['Region'].unique())))
col1, col2= st.columns(2)
with col1:
    df_grouped_by_region_crime_year = df.groupby(['Region', 'Crime', 'Year']).sum(numeric_only=True)['Value'].reset_index()
    df_grouped_by_region_crime_selected = df_grouped_by_region_crime_year.loc[df_grouped_by_region_crime_year['Crime'] == crime_option]
    region_list = df['Region'].unique()
    for region in region_list:
        if region not in region_multiselection:
            df_grouped_by_region_crime_selected = df_grouped_by_region_crime_selected.loc[df_grouped_by_region_crime_selected['Region'] != region]

    fig = px.line(data_frame = df_grouped_by_region_crime_selected,
            x = 'Year',
            y = 'Value',
            color = 'Region',
            title = f"Overall trend in the different regions (absolute values)")
    st.plotly_chart(fig)
with col2:
    df_grouped_by_region_crime_year_incidence = df.groupby(['Region', 'Crime', 'Year']).sum(numeric_only=True)['Value over 100000 population'].reset_index()
    df_grouped_by_region_crime_selected_incidence = df_grouped_by_region_crime_year_incidence.loc[df_grouped_by_region_crime_year_incidence['Crime'] == crime_option]
    region_list = df['Region'].unique()
    for region in region_list:
        if region not in region_multiselection:
            df_grouped_by_region_crime_selected_incidence = df_grouped_by_region_crime_selected_incidence.loc[df_grouped_by_region_crime_selected_incidence['Region'] != region]

    fig = px.line(data_frame = df_grouped_by_region_crime_selected_incidence,
            x = 'Year',
            y = 'Value over 100000 population',
            color = 'Region',
            title = f"Overall trend in the different regions (values over 100000 population)")
    st.plotly_chart(fig) 


#===========================================================================================================================================================

# Second part --> Comparison of different crime rates for different provinces
st.write(f"### Provincial comparison of the '{crime_option}' crime")


# Filtering the df through the crime chosen in the selection box
df_crime = df.loc[df['Crime'] == crime_option]

# Multiselection box to choose the different provinces to compare
province_multiselection = st.multiselect('Choose the provinces you want to compare: ',
                                      (list(df_crime['Province'].unique())))
# Filtering the df through the provinces selected in the multiselection box
province_list = list(df_crime['Province'].unique())
for province in province_list:
    if province not in province_multiselection:
        df_crime = df_crime.loc[df_crime['Province'] != province]

# Dividing the page into two columns, in the first one we are gonna put the line chart with the absolute values, in the second one the line chart with the values over 100.000 population
col1,col2 = st.columns(2)
# Adding line plot with absolute values in the first column
with col1:
    fig = px.line(data_frame = df_crime,
                x = 'Year',
                y = 'Value',
                color = 'Province',
                hover_data = ['Population', 'Value over 100000 population'],
                title = f"Trend of the '{crime_option}' crime over the years (absolute values)")
    st.plotly_chart(fig)
# Adding line plot with values over 100.000 population in the second column
with col2:
    fig = px.line(data_frame = df_crime,
                x = 'Year',
                y = 'Value over 100000 population',
                color = 'Province',
                hover_data = ['Population', 'Value'],
                title = f"Trend of the '{crime_option}' crime over the years (values over 100.000 population)")
    st.plotly_chart(fig)

#===========================================================================================================================================================

# Third part --> Comparison of different crime rates for each province
st.write("## Comparison of different crime rates for each province")

# Selection box to choose a specific province
province_option = st.selectbox('Select a province: ',
                               (list(df['Province'].unique())))
# Using the function get_province_df in order to get a dataframe filtered with the province chosen in the selection box
df_province = functions.get_province_df(df, province_option)

# Multiselection box to choose different types of crime
crime_multiselection = st.multiselect('Choose from the following types of crime',
                                   (list(df_province['Crime'].unique())))

# Slider to choose the year to use for the pie chart
year_selection = st.slider('Select a year for the pie chart: ',
                            min_value=2006,
                            max_value=2021,
                            step=1)

# Filtering the dataframe of the selected province with the selected crimes
crime_list = list(df_province['Crime'].unique())
for crime in crime_list:
    if crime not in crime_multiselection:
        df_province = df_province.loc[df_province['Crime'] != crime]

# Dividing the page into two columns, in the first one we are gonna put the line chart while in the second one we are gonna put the pie chart
# Creating two columns
col1, col2 = st.columns(2)
# Adding line plot in the first column
with col1:
    fig = px.line(data_frame = df_province,
                x = 'Year',
                y = 'Value',
                color = 'Crime',
                title= f"Trend of the selected crimes in the province of {province_option} from 2006 to 2021 (absolute values)")
    st.plotly_chart(fig)
# Adding pie chart in the second column
with col2:
    df_province_year = df_province.loc[df_province['Year'] == year_selection]
    fig = px.pie(data_frame= df_province_year,
                 values = 'Value', 
                 names = 'Crime',
                 color = 'Crime',
                 title = f"Distribution of the selected crimes in the province of {province_option} for year {year_selection}")
    st.plotly_chart(fig)


st.write("## Comparison of different crime rates for each region")
st.write('You selected: ', crime_multiselection)
# Selection box to choose a specific province
region_option = st.selectbox('Select a province: ',
                               (list(df['Region'].unique())))
# Using the function get_province_df in order to get a dataframe filtered with the province chosen in the selection box
df_region = functions.get_region_df(df, region_option)

# Slider to choose the year to use for the pie chart
year_selection2 = st.slider('Select a year for the pie chart: ',
                            min_value=2006,
                            max_value=2021,
                            step=1,
                            key='5')

for crime in crime_list:
    if crime not in crime_multiselection:
        df_region = df_region.loc[df_region['Crime'] != crime]

# Dividing the page into two columns, in the first one we are gonna put the line chart while in the second one we are gonna put the pie chart
# Creating two columns
col1, col2 = st.columns(2)
# Adding line plot in the first column
with col1:
    df_region = df_region.groupby(['Region', 'Crime','Year']).sum(numeric_only=True).reset_index()
    fig = px.line(data_frame = df_region,
                x = 'Year',
                y = 'Value',
                color = 'Crime',
                title= f"Trend of the selected crimes in the region of {region_option} from 2006 to 2021 (absolute values)")
    st.plotly_chart(fig)
# Adding pie chart in the second column
with col2:
    df_region_year = df_region.loc[df_region['Year'] == year_selection2]
    df_region_year = df_region_year.groupby(['Region', 'Crime']).sum(numeric_only=True).reset_index()
    fig = px.pie(data_frame= df_region_year,
                 values = 'Value', 
                 names = 'Crime',
                 color = 'Crime',
                 title = f"Distribution of the selected crimes in the region of {region_option} for year {year_selection}")
    st.plotly_chart(fig)


st.write("## Comparison of different crime rates for each macro-area")
st.write('You selected: ', crime_multiselection)
# Selection box to choose a specific province
area_option = st.selectbox('Select a macro-area: ',
                               (list(df['Area'].unique())))
# Using the function get_province_df in order to get a dataframe filtered with the province chosen in the selection box
df_area = functions.get_zone_df(df, area_option)

# Slider to choose the year to use for the pie chart
year_selection3 = st.slider('Select a year for the pie chart: ',
                            min_value=2006,
                            max_value=2021,
                            step=1,
                            key='8')

for crime in crime_list:
    if crime not in crime_multiselection:
        df_area = df_area.loc[df_area['Crime'] != crime]

# Dividing the page into two columns, in the first one we are gonna put the line chart while in the second one we are gonna put the pie chart
# Creating two columns
col1, col2 = st.columns(2)
# Adding line plot in the first column
with col1:
    df_area = df_area.groupby(['Area', 'Crime','Year']).sum(numeric_only=True).reset_index()
    fig = px.line(data_frame = df_area,
                x = 'Year',
                y = 'Value',
                color = 'Crime',
                title= f"Trend of the selected crimes in the {area_option} area from 2006 to 2021 (absolute values)")
    st.plotly_chart(fig)
# Adding pie chart in the second column
with col2:
    df_area_year = df_area.loc[df_area['Year'] == year_selection3]
    df_area_year = df_area_year.groupby(['Area', 'Crime']).sum(numeric_only=True).reset_index()
    fig = px.pie(data_frame= df_area_year,
                 values = 'Value', 
                 names = 'Crime',
                 color = 'Crime',
                 title = f"Distribution of the selected crimes in the {area_option} area for year {year_selection}")
    st.plotly_chart(fig)
#===========================================================================================================================================================