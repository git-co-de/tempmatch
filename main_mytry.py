import streamlit as st
import api_mytry
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from io import BytesIO

from data_mytry import get_daily, get_hourly


st.set_page_config(layout = "wide")
sns.set_theme(style = "whitegrid")

st.header('City TempMatch')
st.write('Compare the temperatures of several places in the world. All temperatures are displayed in °Celcius.')

st.sidebar.header('Customize your request')

map     = st.sidebar.checkbox('Worldmap')
cities  = st.sidebar.text_input('Choose cities', placeholder = 'city1 city2 ...')
start   = st.sidebar.date_input('Start Date')
end     = st.sidebar.date_input('End Date')

intervall = st.sidebar.selectbox('Select the temperature intervall displayed', ['by hour', 'by day'])


dataframe = []
gps = pd.DataFrame(columns = ['lat', 'lon'])

col1, col2 = st.columns([2,1])

with col1:

    if cities: 
        for city in cities.split():
            data = api_mytry.fetch_data_city(city, start, end)
            
            # Debugging: API-Antwort anzeigen
            #st.write(f"Data for city '{city}':", data)

            # Prüfen, ob GPS-Daten vorhanden sind
            if "latitude" in data and "longitude" in data:
                gps.loc[len(gps)] = [data["latitude"], data["longitude"]]
            else:
                st.error(f"Could not fetch latitude/longitude for city '{city}'.")
                continue

            if intervall == 'by hour':
                df = get_hourly(data)
            elif intervall == 'by day':
                df = get_daily(data)

            dataframe.append(df)

        fig, ax1 = plt.subplots(figsize = (6,6))

        for d in dataframe:
            d.plot(
                kind = "line", 
                ax = ax1,
                ylabel = "temperature", 
                xlabel = "date",
                rot = 90,
                fontsize = 8)
            if intervall == "by hour":
                ticks = range(0, len(d), 24)
            
            elif intervall == "by day":
                ticks = range(0, len(d))

        buf = BytesIO()
        fig.savefig(buf, format = 'png')

        st.image(buf)

with col2: 
    if map: 
        st.header("Worldmap")
        st.map(gps)