
# References: https://github.com/zakariachowdhury/streamlit-map-dashboard/
# US State Boundaries: https://public.opendatasoft.com/explore/dataset/us-state-boundaries/export/

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

APP_TITLE = 'Natural Disaster Prediction in the United States'
APP_SUB_TITLE = 'AIPI 510 Project Developed By: Nicholas Conterno, Sri Veerisetti and Zach Xing '

def display_time_filters(df):
    year_list = list(df['Year'].unique())
    year_list.sort()
    year = st.sidebar.selectbox('Year', year_list, len(year_list)-1)
    if year == 2024:
        st.header(f'{year} Prediction')
    else:
        st.header(f'{year}')
    # return year, quarter
    return year

def display_state_filter(df, state_name):
    state_list = [''] + list(df['State Name'].unique())
    if '0' in state_list:
        state_list.remove('0')
    state_list.sort()
    state_index = state_list.index(state_name) if state_name and state_name in state_list else 0
    return st.sidebar.selectbox('State', state_list, state_index)

def display_risk_level():
    return st.sidebar.radio('Risk Levels', ['All', 'Low', 'Medium', 'High'])

def display_map(df, year):
    df = df[(df['Year'] == year)]

    map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')
    
    choropleth = folium.Choropleth(
        geo_data='data/us-state-boundaries.geojson',
        data=df,
        columns=('State Name', 'Total Deaths'),
        key_on='feature.properties.name',
        fill_color="Reds",
        fill_opacity=0.7,
        line_opacity=0.8,
        legend_name="Reports",
        highlight=True
    )
    choropleth.geojson.add_to(map)

    df_indexed = df.set_index('State Name')
    
    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['name']
        _data = df_indexed.loc[state_name, 'Total Deaths'] if state_name in list(df_indexed.index) else 0
        # print(_data)
        feature['properties']['Total Deaths'] = 'Total Deaths: ' + '{:,}'.format(df_indexed.loc[state_name, 'Total Deaths']) if state_name in list(df_indexed.index) else ''
        feature['properties']['Total Damage (\'000 US$)'] = 'Total Damage (\'000 US$): ' + str(round(df_indexed.loc[state_name, 'Total Damage (\'000 US$)'])) if state_name in list(df_indexed.index) else ''
        feature['properties']['Total Disasters'] = 'Total Disasters: ' + str(round(df_indexed.loc[state_name, 'Total Disasters'])) if state_name in list(df_indexed.index) else ''
        feature['properties']['No. Injured'] = 'No. Injured: ' + str(round(df_indexed.loc[state_name, 'No. Injured'])) if state_name in list(df_indexed.index) else ''


    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name', 'Total Deaths', 'Total Damage (\'000 US$)', 'Total Disasters', 'No. Injured'], labels=False) 
    )
    
    st_map = st_folium(map, width=700, height=450)

    state_name = ''
    if st_map['last_active_drawing']:
        state_name = st_map['last_active_drawing']['properties']['name']
    return state_name

def display_disater(df, year, state_name, field, title, string_format='{:,}', is_median=False):
    df = df[(df['Year'] == year)]
    if state_name:
        df = df[df['State Name'] == state_name]
    # df.drop_duplicates(inplace=True)
    if is_median:
        total = df[field].sum() / len(df[field]) if len(df) else 0
    else:
        total = df[field].sum()
    st.metric(title, string_format.format(round(total)))

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    #Load Data
    # df_continental = pd.read_csv('data/AxS-Continental_Full Data_data.csv')
    df_continental = pd.read_csv('my_data/merged.csv')

    #Display Filters and Map
    year = display_time_filters(df_continental)
    if year == 2024:
        risk_level = display_risk_level()
        if risk_level == 'Low':
            df_continental = df_continental[df_continental['Risk Level'] == 1]
        elif risk_level == 'Medium':
            df_continental = df_continental[df_continental['Risk Level'] == 2]
        elif risk_level == 'High':
            df_continental = df_continental[df_continental['Risk Level'] == 3]
        elif risk_level == 'All':
            df_continental = df_continental
    state_name = display_map(df_continental, year)
    state_name = display_state_filter(df_continental, state_name)
    

    # Display Metrics
    st.subheader(f'{state_name} Details')

    col1, col2, col3 = st.columns(3)
    with col1:
        display_disater(df_continental, year, state_name, 'Total Deaths', 'Total Deaths', string_format='{:,}')
    with col2:
        display_disater(df_continental, year, state_name, 'Total Damage (\'000 US$)', 'Total Damage (\'000 US$)')
    with col3:
        display_disater(df_continental, year, state_name, 'Total Disasters', 'Total Disasters')
    # with col4:
    #     display_disater(df_continental, year, state_name, 'No. Injured', 'No. Injured')


if __name__ == "__main__":
    main()