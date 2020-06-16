from flask import Flask
import folium

app = Flask(__name__)

@app.route("/")
def index():
    folium_map = folium.Map(location=[46,2.291705], zoom_start=7)
    return folium_map._repr_html_()

if __name__ == "__main__":
    app.run()