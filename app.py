import streamlit as st
import pandas as pd
import pydeck as pdk

def simple_map(filtered_df):
  st.map(filtered_df, latitude='Lat', longitude='Lon', color='color', size=100)

def pydeck_map(df):
  locations = pd.DataFrame({'lon': df['Lon'], 'lat': df['Lat']})

  st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.data_utils.compute_view(locations),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[Lon, Lat]',
            get_fill_color='color',
            get_radius=7,
            radius_units='"pixels"', # See https://deckgl.readthedocs.io/en/latest/layer.html#understanding-keyword-arguments-in-pydeck-layers
            pickable=True
        ),
    ],
    height=3500,
    tooltip={'html': '<div>Casualty type: {CasualtyTypeFull}</div><div>Reason for launch: {ReasonforLaunch}</div><div>Outcome: {OutcomeOfService}</div><div>Weather: {WeatherAtIncident}</div><div>Date: {DateOfLaunch}</div>'}
  ))

st.set_page_config(layout="wide")
st.title("RNLI Launches 2019-2023")

df = pd.read_csv('./RNLI_Return_of_Service.csv', usecols=['LifeboatStationNameProper', 'AIC', 'LifeboatClass', 'CasualtyTypeFull', 'ReasonforLaunch', 'OutcomeOfService', 'Activity', 'WeatherAtIncident', 'DateOfLaunch', 'x', 'y'])
df = df.rename(columns={'LifeboatStationNameProper': 'Station', 'x': 'Lon', 'y': 'Lat'})

station_names = df['Station'].unique()
station_names.sort()
selected_station = st.selectbox('Station', station_names)

filtered_df = df[df['Station'] == selected_station]

outcome_colors = {
  "Rendered assistance": [17,119,51],
  "Others assisted casualty": [68,170,153],
  "Stood down": [170,68,153],
  "Unsuccessful search": [136,34,85],
  "False alarm": [204,102,119],
  "Unknown": [85,85,85]
}

filtered_df['color'] = filtered_df.apply(lambda row: outcome_colors[row["OutcomeOfService"]], axis=1)

# Legend?

# simple_map(filtered_df)
pydeck_map(filtered_df)
