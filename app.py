from flask import Flask
import model

app = Flask(__name__)

@app.route("/")
def index():
    folium_map = model.get_map()
    return folium_map._repr_html_()

if __name__ == "__main__":
    app.run()