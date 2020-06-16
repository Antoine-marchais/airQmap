import folium

def get_map():
    folium_map = folium.Map(location=[46,2.291705], zoom_start=7)
    return folium_map