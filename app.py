import pandas as pd
import streamlit as st
import pydeck as pdk

df_school_profile = pd.read_excel('./data/School Profile 2024.xlsx', sheet_name='SchoolProfile 2024')
df_school_loc = pd.read_excel('./data/School Location 2024.xlsx', sheet_name='SchoolLocations 2024')


st.set_page_config(layout="wide")


st.dataframe(df_school_loc)


INITIAL_VIEW_STATE = pdk.ViewState(
  latitude=-33.865143   ,
  longitude=151.209900,
  zoom=11,
  max_zoom=16,
  pitch=45,
  bearing=0
)


r = pdk.Deck(
        initial_view_state=INITIAL_VIEW_STATE,
        map_style="dark"
)

st.pydeck_chart(r)