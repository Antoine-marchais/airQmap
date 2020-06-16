import folium
from enum import Enum

class Pollutant(Enum):
    NO2 = 8
    SO2 = 1
    PM10 = 5
    O3 = 7
    NOX = 9
    CO = 10
    H2S = 11
    PM25 = 6001 