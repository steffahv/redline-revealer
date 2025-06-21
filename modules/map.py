"""Redlining Map Page for Redline Revealer.

Displays interactive overlays of historical redlining and housing risk.
Powered by Azure Maps with a Folium fallback.
"""

import os
import geopandas as gpd
import streamlit as st
from utils.azure_map import AzureMapRenderer
from streamlit_folium import st_folium
import folium
from folium.plugins import Search

def render():
    st.set_page_config(layout="wide", page_title="Redlining Visualizer", page_icon="📍")
    st.title("📍 Redlining Map Viewer")

    @st.cache_data
    def load_data():
        """Load redlining GeoJSON data from fallback paths."""
        paths_to_try = [
            os.path.join("data", "HOLC_Atlanta_GA.geojson"),
            os.path.join("data", "merged_housing_data.geojson")
        ]
        for path in paths_to_try:
            if os.path.exists(path):
                return gpd.read_file(path)
        st.error("No redlining data found in expected paths.")
        st.stop()

    holc_gdf = load_data()

    map_type = st.sidebar.radio(
        "Map Provider",
        ("Azure Maps", "Folium (Fallback)"),
        index=0 if st.secrets.get("AZURE_MAPS_KEY") else 1
    )

    if map_type == "Azure Maps":
        renderer = AzureMapRenderer()
        map_url = renderer.render(holc_gdf.__geo_interface__)
        if map_url:
            st.components.v1.iframe(map_url, height=700)
        else:
            st.warning("Azure Maps failed — falling back to Folium")
            st_folium(create_folium_map(holc_gdf), width=1200, height=700)
    else:
        st_folium(create_folium_map(holc_gdf), width=1200, height=700)

    st.sidebar.subheader("Statistics")
    grade_counts = holc_gdf['grade'].value_counts()
    st.sidebar.metric("Total Areas", len(holc_gdf))
    st.sidebar.metric("A-Grade Areas", grade_counts.get('A', 0))
    st.sidebar.metric("D-Grade Areas", grade_counts.get('D', 0))


def create_folium_map(gdf):
    """Create a Folium-based fallback map."""
    m = folium.Map(location=[33.749, -84.388], zoom_start=11)
    folium.GeoJson(
        gdf,
        style_function=lambda f: {
            'fillColor': {
                'A': '#00FF00', 'B': '#FFFF00',
                'C': '#FFA500', 'D': '#FF0000'
            }.get(f['properties']['grade'], '#CCCCCC'),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        }
    ).add_to(m)
    return m
