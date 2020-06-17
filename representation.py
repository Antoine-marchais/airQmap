import folium
from folium.plugins import HeatMapWithTime, TimestampedGeoJson
from branca.colormap import LinearColormap
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

def heatmap(pollutant):
    """
    Returns a heatmap with time of the pollutant levels at each station

    Returns:
        Map: folium heatmap with time
    """
    folium_map = folium.Map(location=[46,2.291705], zoom_start=7)
    client = DBClient()
    ordered_mesures = client.get_mesures_by_time(pollutant)
    global_max = get_global_max(ordered_mesures)
    heatmap_data = []
    heatmap_index = []
    for time in ordered_mesures:
        heatmap_data.append([[mesure["position"]["x"], mesure["position"]["y"], mesure["value"]/global_max] for mesure in ordered_mesures[time]])
        heatmap_index.append(dt.datetime.strftime(time,"%d/%m %H:%M:%S"))
    HeatMapWithTime(heatmap_data, position="topright", index=heatmap_index).add_to(folium_map)
    return folium_map

def value_map(pollutant):
    """
    Returns a map with mesures values and their location for each instant

    Args:
        pollutant (string): name of the pollutant to display

    Returns:
        Map: folium map with time mesures
    """
    folium_map = folium.Map(location=[46,2.291705], zoom_start=7)
    client = DBClient()
    ordered_mesures = client.get_mesures_by_time(pollutant)
    global_max = get_global_max(ordered_mesures)

    encoder = JSONEncoder(global_max)
    features = []
    for time in ordered_mesures:
        features += [encoder.encode_as_geoJSON(mesure) for mesure in ordered_mesures[time]]

    tsjson = TimestampedGeoJson(
        {'type': 'FeatureCollection',
        'features': features}, 
        period='PT1H', 
        add_last_point=True, 
        auto_play=False, 
        loop=False,
        max_speed=1, 
        loop_button=True, 
        time_slider_drag_update=True
    )
    tsjson.options["position"]="topright"
    tsjson.add_to(folium_map)
    encoder.cm.caption=f"{pollutant} concentration in ug.m-3"
    folium_map.add_children(encoder.cm)
    return folium_map

class JSONEncoder:
    """
    Encoder for geoJSON features with time dimension
    """

    def __init__(self, max_value):
        """
        Initialize encode

        Args:
            max_value (float): maximum value for encoded features
        """
        self.cm = LinearColormap(["green","yellow","red"], vmin=0, vmax=max_value)
    
    def encode_as_geoJSON(self, mesure):
        """
        encode a mesure as geoJSON

        Args:
            mesure (Dict): mesure dictionary as encoded in the db

        Returns:
            Dict: GeoJSON encoded feature
        """
        color = self.cm(mesure["value"])
        return {
        'type': 'Feature',
        'geometry': {
            'type':'Point', 
            'coordinates':[mesure["position"]["y"], mesure["position"]["x"]]
        },
        'properties': {
            'time': mesure["end_mesure"].isoformat(),
            'style': {'color' : color},
            'icon': 'circle',
            'iconstyle':{
                'fillColor': color,
                'fillOpacity': 0.8,
                'stroke': 'true',
                'radius': 7
            }
        }
    }

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

