# Libraries
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

# Header and description
st.markdown('''
         ## 1. Trend of each type of crime on different levels: ***overall***, ***macro-area***, ***regional*** and ***provincial***
         ''')
st.write('Select a crime typology and see its overall trend around the Italian territory at different levels: ***provincial***, ***regional***, ***macro-area***, ***overall***.')

# Select box to choose the type of crime
crime_option = st.selectbox('Choose the type of crime: ',
                            (list(df['Crime'].unique())))

tab1, tab2, tab3, tab4 = st.tabs(['Provincial', 'Regional', 'Macro-Area', 'Overall'])

# Comparison of different crime rates for different provinces
tab1.write(f"### Provincial comparison of the '{crime_option}' crime")
tab1.markdown('''
            With reference to the crime chosen above, see its overall trend around the different Italian **provinces**:
            * On the upper chart, **absolute values** are taken into consideration;
            * On the lower chart, **values over 100'000 inhabitants** are taken into consideration.
            ''')

# Filtering the df through the crime chosen in the selection box
df_crime = df.loc[df['Crime'] == crime_option]

# Multiselection box to choose the different provinces to compare
province_multiselection = tab1.multiselect('Choose the provinces you want to compare: ',
                                      (list(df_crime['Province'].unique())))
# Filtering the df through the provinces selected in the multiselection box
province_list = list(df_crime['Province'].unique())
for province in province_list:
    if province not in province_multiselection:
        df_crime = df_crime.loc[df_crime['Province'] != province]

fig = px.line(data_frame = df_crime,
            x = 'Year',
            y = 'Value',
            color = 'Province',
            hover_data = ['Population', 'Value over 100000 population'],
            title = f"Trend of the '{crime_option}' crime over the years (absolute values)")
tab1.plotly_chart(fig, use_container_width= True)

fig = px.line(data_frame = df_crime,
            x = 'Year',
            y = 'Value over 100000 population',
            color = 'Province',
            hover_data = ['Population', 'Value'],
            title = f"Trend of the '{crime_option}' crime over the years (values over 100.000 population)")
tab1.plotly_chart(fig, use_container_width= True)

# ============================================================================================================================================================================

tab2.write(f"### Regional comparison of the '{crime_option}' crime")
tab2.markdown('''
            With reference to the crime chosen above, see its overall trend around the different Italian **regions**:
            * On the upper chart, **absolute values** are taken into consideration;
            * On the lower chart, **values over 100'000 inhabitants** are taken into consideration.
            ''')
# Multiselection box to select the regions
region_multiselection = tab2.multiselect('Choose the regions you want to compare: ',
                                       (list(df['Region'].unique())))

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
tab2.plotly_chart(fig, use_container_width= True)

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
tab2.plotly_chart(fig, use_container_width= True)

# ======================================================================================================================================

# Header and description
tab3.write(f"### Macro-area comparison of the '{crime_option}' crime")
tab3.markdown('''
            With reference to the crime chosen above, see its overall trend around the different Italian **macro-areas**:
            * On the upper chart, **absolute values** are taken into consideration;
            * On the lower chart, **values over 100'000 inhabitants** are taken into consideration.
            ''')

# Multiselection box to select the areas to compare
area_multiselection = tab3.multiselect('Choose the areas you want to compare: ',
                                     (list(df['Area'].unique())))

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
tab3.plotly_chart(fig, use_container_width= True)


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
tab3.plotly_chart(fig, use_container_width= True)

#===========================================================================================================================================================
tab4.write(f"### Overall comparison of the '{crime_option}' crime")
tab4.markdown('''
            With reference to the crime chosen above, see its overall trend around the whole Italian territory.
            ''')
# Creating a DF grouped by Crime and Year and with the values summed through all the areas
df_grouped_by_crime_year = df.groupby(['Crime', 'Year']).sum(numeric_only= True)['Value'].reset_index()
# Filtering the DF with the selected crime
df_grouped_by_crime_selected = df_grouped_by_crime_year.loc[df_grouped_by_crime_year['Crime'] == crime_option]

# Plotly line chart
fig = px.line(data_frame = df_grouped_by_crime_selected,
            x = 'Year',
            y = 'Value',
            color = 'Crime',
            title = f"Overall trend over the years (absolute values)")
# Displaying the plot
tab4.plotly_chart(fig, use_container_width = True)

#===========================================================================================================================================================
st.divider()
#===========================================================================================================================================================

# Second part --> Comparison of different crime rates for each province
st.write('''
         ## 2. Comparison of different crime rates at different levels: *provincial*, *regional* and *macro-area*
         ''')
st.write('''
        In this section, select multiple crime types and compare the trends at different levels: ***provincial***, ***regional*** and ***macro-area***.
         ''')

# Multiselection box to choose different types of crime
crime_multiselection = st.multiselect('Choose from the following types of crime:',
                                   (list(df['Crime'].unique())))

tab5, tab6, tab7 = st.tabs(['Provincial', 'Regional', 'Macro-Area'])
tab5.write(f"### Provincial comparison of the '{crime_multiselection}' crimes")
tab5.markdown('''
            With reference to the crimes chosen above, see their overall trend around a specific Italian **province**.
            ''')
# Selection box to choose a specific province
province_option = tab5.selectbox('Select a province: ',
                               (list(df['Province'].unique())))
# Using the function get_province_df in order to get a dataframe filtered with the province chosen in the selection box
df_province = functions.get_province_df(df, province_option)

# Filtering the dataframe of the selected province with the selected crimes
crime_list = list(df_province['Crime'].unique())
for crime in crime_list:
    if crime not in crime_multiselection:
        df_province = df_province.loc[df_province['Crime'] != crime]

fig = px.line(data_frame = df_province,
            x = 'Year',
            y = 'Value',
            color = 'Crime',
            title= f"Trend of the selected crimes in the province of {province_option} from 2006 to 2021 (absolute values)")
tab5.plotly_chart(fig, use_container_width= True)

#===========================================================================================================================================================

tab6.write(f"### Regional comparison of the '{crime_multiselection}' crimes")
tab6.markdown('''
            With reference to the crimes chosen above, see their overall trend around a specific Italian **region**.
            ''')
# Selection box to choose a specific province
region_option = tab6.selectbox('Select a province: ',
                               (list(df['Region'].unique())))
# Using the function get_province_df in order to get a dataframe filtered with the province chosen in the selection box
df_region = functions.get_region_df(df, region_option)

for crime in crime_list:
    if crime not in crime_multiselection:
        df_region = df_region.loc[df_region['Crime'] != crime]

df_region = df_region.groupby(['Region', 'Crime','Year']).sum(numeric_only=True).reset_index()
fig = px.line(data_frame = df_region,
            x = 'Year',
            y = 'Value',
            color = 'Crime',
            title= f"Trend of the selected crimes in the region of {region_option} from 2006 to 2021 (absolute values)")
tab6.plotly_chart(fig, use_container_width= True)

#===========================================================================================================================================================

tab7.write(f"### Macro-area comparison of the '{crime_multiselection}' crimes")
tab7.markdown('''
            With reference to the crimes chosen above, see their overall trend around a specific Italian **macro-area**
            ''')
# Selection box to choose a specific province
area_option = tab7.selectbox('Select a macro-area: ',
                               (list(df['Area'].unique())))
# Using the function get_province_df in order to get a dataframe filtered with the province chosen in the selection box
df_area = functions.get_zone_df(df, area_option)

for crime in crime_list:
    if crime not in crime_multiselection:
        df_area = df_area.loc[df_area['Crime'] != crime]

df_area = df_area.groupby(['Area', 'Crime','Year']).sum(numeric_only=True).reset_index()
fig = px.line(data_frame = df_area,
            x = 'Year',
            y = 'Value',
            color = 'Crime',
            title= f"Trend of the selected crimes in the {area_option} area from 2006 to 2021 (absolute values)")
tab7.plotly_chart(fig, use_container_width= True)

st.divider()
#===========================================================================================================================================================

st.write('''
         ## 3. Linear Regression
         ''')
st.write('''
In this **linear regression** example made with Plotly the relationship between population and crime rates is shown to demonstrate that the higher the population, the higher the rates.
         ''')

# Scatter plot and linear regression with Plotly and Statsmodels
fig = px.scatter(data_frame= df.groupby(['Province', 'Year', 'Population']).sum(numeric_only=True)['Value'].reset_index(),
           x = 'Population',
           y = 'Value',
           color= 'Province',
           hover_data= ['Province', 'Year'],
           trendline= "ols",
           trendline_scope= 'overall',
           title = 'Relationship between population and crime rates')

st.plotly_chart(fig, use_container_width= True)