import folium
from folium.plugins import HeatMapWithTime

def blank_map():
    folium_map = folium.Map(location=[46,2.291705], zoom_start=7)
    return folium_map

def heatmap():
    folium_map = folium.Map(location=[46,2.291705], zoom_start=7)
    return folium_map