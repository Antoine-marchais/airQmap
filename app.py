from flask import Flask, request
import representation

app = Flask(__name__)

@app.route("/blank")
def get_blank():
    folium_map = representation.blank_map()
    return folium_map._repr_html_()

@app.route("/heatmap")
def get_heat():
    folium_map = representation.heatmap(request.args.get("pollutant"))
    return folium_map._repr_html_()

@app.route("/values")
def get_values():
    folium_map = representation.value_map(request.args.get("pollutant"))
    return folium_map._repr_html_()

if __name__ == "__main__":
    app.run()