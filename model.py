import folium
from enum import Enum

def get_map():
    folium_map = folium.Map(location=[46,2.291705], zoom_start=7)
    return folium_map

class Pollutant(Enum):
    NO2 = 8
    SO2 = 1
    PM10 = 5
    O3 = 7
    NOX = 9
    CO = 10
    H2S = 11
    PM25 = 6001 