import folium
from folium.plugins import HeatMapWithTime
from model import DBClient
import datetime as dt

def blank_map():
    """
    Returns a blank map adjusted to France

    Returns:
        Map: blank folium map
    """
    folium_map = folium.Map(location=[46,2.291705], zoom_start=7)
    return folium_map

def heatmap():
    """
    Returns a heatmap with time of the pollutant levels at each station

    Returns:
        Map: folium heatmap with time
    """
    folium_map = folium.Map(location=[46,2.291705], zoom_start=7)
    client = DBClient()
    ordered_mesures = client.get_mesures_by_time("NO2")
    global_max = get_global_max(ordered_mesures)
    heatmap_data = []
    heatmap_index = []
    for time in ordered_mesures:
        heatmap_data.append([[mesure["position"]["x"], mesure["position"]["y"], mesure["value"]/global_max] for mesure in ordered_mesures[time]])
        heatmap_index.append(dt.datetime.strftime(time,"%d/%m %H:%M:%S"))
    HeatMapWithTime(heatmap_data, index=heatmap_index).add_to(folium_map)
    return folium_map

def get_global_max(ordered_mesures):
    """
    Get the maximum of all mesures in the object

    Args:
        ordered_mesures (OrderedDict): dict of all mesures ordered by time

    Returns:
        float: global maximum
    """
    mesurement_max = 0
    for mesures_at_t in ordered_mesures.values():
        values_at_t = [mesure["value"] for mesure in mesures_at_t]
        mesurement_max = max(mesurement_max, max(values_at_t))
    return mesurement_max