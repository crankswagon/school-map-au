import pandas as pd
import streamlit as st
import pydeck as pdk
from sklearn import preprocessing
import geopandas as gpd
import math


## load in data
df_school_profile = pd.read_excel('./data/School Profile 2024.xlsx', sheet_name='SchoolProfile 2024')
df_school_profile.set_index("ACARA SML ID", inplace=True)
df_school_loc = pd.read_excel('./data/School Location 2024.xlsx', sheet_name='SchoolLocations 2024')
df_school_loc.set_index("ACARA SML ID", inplace=True)
df_vis = df_school_profile.join(df_school_loc, rsuffix="_locd")
drop_cols = [x for x in df_vis.columns if x.endswith("_locd")]
_discard = [df_vis.pop(_) for _ in drop_cols] 


## load in catchment shapefile
# gdf = gpd.read_file("./data/catchments_primary.shp")

## make more metrics
df_vis["Student Teacher Ratio"] = df_vis["Total Enrolments"]/df_vis["Full Time Equivalent Teaching Staff"]


## NSW Shapefile https://data.nsw.gov.au/data/dataset/nsw-education-school-intake-zones-catchment-areas-for-nsw-government-schools



## normalisation for vis
color_scaler = preprocessing.MaxAbsScaler()

# x_scaled = min_max_scaler.fit_transform(df_vis)
# df = pd.DataFrame(x_scaled)

# st.dataframe(df_school_loc)
# st.dataframe(df_school_profile)





# st.dataframe(gdf)

INITIAL_VIEW_STATE = pdk.ViewState(
  latitude=-33.865143   ,
  longitude=151.209900,
  zoom=11,
  max_zoom=16,
  pitch=45,
  bearing=0
)





tooltip = {
   "html": "<b>School Name:</b> {School Name} <br/> \
            <b>Student Teacher Ratio:</b> {Student Teacher Ratio} <br/>\
            <b>ICSEA Percentile:</b> {ICSEA Percentile} <br/>",
   "style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }
}

# nsw_catchment = pdk.Layer(
#     'GeoJsonLayer',
#     gdf,
#     opacity=0.3,
#     stroked=False,
#     get_polygon='Geometry',
#     filled=True,
#     extruded=True,
#     wireframe=True,
#     # get_elevation=
#     pickable=True,
#     auto_highlight=True,
#     get_line_color=[255, 255, 255],
#     get_fill_color = [255, 100, 100, 100]

# )

def app():
    st.set_page_config(layout="wide")
    
    ## Selectors
    
    with st.sidebar:   
        states = st.multiselect("States", df_vis["State"].unique(), default=df_vis["State"].unique())
        schoolType = st.multiselect("School Type", df_vis["School Type"].unique(), default=df_vis["School Type"].unique())
        schoolSector = st.multiselect("School Sector", df_vis["School Sector"].unique(), default=df_vis["School Sector"].unique())
        # st.write("State limited to:", states)
        
        colourBy = st.selectbox("Render Map Using:", ["ICSEA"])
        colourBalance = 155 + st.select_slider("Stratification Sensitivity:", range(25,90), value = 65 ) #220 
        st.write("Increase stratification sensitivity to visually identify top performers")
        
    
    filtered_df_vis = df_vis[df_vis['State'].isin(states) & \
                             df_vis['School Type'].isin(schoolType) &\
                             df_vis['School Sector'].isin(schoolSector)
                                 ]
    
    
    filtered_df_vis["clr"] = color_scaler.fit_transform(filtered_df_vis[[colourBy]])*255
    filtered_df_vis["radius"] = filtered_df_vis["Total Enrolments"].apply(lambda x: math.sqrt(x))

    # st.vega_lite_chart(
    #             filtered_df_vis,
    #             {
    #                 "mark": "bar", #{"type": "circle", "tooltip": True},
    #                     "encoding": {
    #                         "x": {
    #                         "bin": "true",
    #                         "field": "clr"
    #                         },
    #                         "y": {"aggregate": "count"}
    #                     }
    #             },
    #             )
    

    # st.dataframe(sample_df)
    
    schools = pdk.Layer(
                    'ScatterplotLayer',     # Change the `type` positional argument here
                    filtered_df_vis,
                    get_position=['Longitude', 'Latitude'],
                    auto_highlight=True,
                    stroked=True,
                    radius_scale=3,
                    # radius_min_pixels=1,
                    # radius_max_pixels=100,
                    get_radius='radius',          # Radius is given in meters
                    get_fill_color=['140', f'clr > {colourBalance} ? 255-2*(255-clr) : 100', f'clr > {colourBalance} ? 100 : 255-2*(255-clr)', '255'],
                    pickable=True)
                    
    r = pdk.Deck(
        initial_view_state=INITIAL_VIEW_STATE,
        layers=[schools],
        map_style="dark",
        tooltip=tooltip
    )
        
      
    st.pydeck_chart(r)
    
    st.dataframe(filtered_df_vis)
    
        
    st.vega_lite_chart(
    filtered_df_vis,
    {
        "mark": "bar", #{"type": "circle", "tooltip": True},
            "encoding": {
                "x": {
                "bin": "true",
                "field": colourBy
                },
                "y": {"aggregate": "count"}
            }
    },
    )
    
    
    

app()
	