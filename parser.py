from bs4 import BeautifulSoup
import pickle as pkl
import argparse
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def parse_stations(path_to_stations):
    """Parse a station xml and return the id and geographical coordinates of each station

    Args:
        path_to_stations (string): path to the xml

    Returns:
        list(dict): list of all stations with their id and coordinates
    """
    with open(path_to_stations,"r") as f:
        station_xml = f.read()

    soup = BeautifulSoup(station_xml, "xml")
    elts = soup.find_all("gml:Point")
    stations = []
    for elt in elts : 
        station = {}
        station["id"] = elt["gml:id"].split("-")[-1]
        station["position"] = [float(coord) for coord in elt.find("gml:pos").string.split()]
        stations.append(station)
    return stations

def parse_mesures(path_to_mesures, path_to_stations):
    """
    Parse a mesure xml using a previously parsed stations xml

    Args:
        path_to_mesures (string): path to the mesures as a xml file
        path_to_stations (string): path to the stations as a parsed binary file

    Returns:
        list(dict): list of mesures with the geographical coordinates of mesure points
    """
    with open(path_to_mesures,"r") as f:
        last_mesures_xml = f.read()

    with open(path_to_stations,"rb") as f:
        stations = pkl.load(f)
    stations_df = pd.DataFrame(stations)

    soup = BeautifulSoup(last_mesures_xml, "xml")
    elts = soup.find_all("om:OM_Observation")
    mesures = []
    for elt in elts :
        mesure_batch = []
        try :
            values = elt.find("swe:values").string.split("@@")[:-1]
            for value in values : 
                mesure = {}
                mesure["date_mesure"] = value.split(",")[0]
                mesure["value"] = value.split(",")[4]
                mesure["station_id"] = elt.find("om:name",{"xlink:href":"http://dd.eionet.europa.eu/vocabulary/aq/processparameter/SamplingPoint"}).find_next()["xlink:href"]
                mesure["position"] = {}
                station_id = mesure["station_id"].split("/")[-1].split("-")[-1]
                position = get_station_coords(station_id, stations_df)
                mesure["position"]["x"] = position[0]
                mesure["position"]["y"] = position[1]
                mesure_batch.append(mesure)
            mesures += mesure_batch
        except:
            logger.debug(f"unable to parse the following element :\n {elt.prettify()}")
    return mesures

def get_station_coords(station_id, stations_df):
    """find the station coordinates using its id

    Args:
        station_id (string): id of the station
        stations_df (pd.Dataframe): dataframe of all stations

    Returns:
        [int, int]: latitude and longitude of the station
    """
    return stations_df.loc[stations_df.id==station_id]["position"].iloc[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path of the document to parse")
    parser.add_argument("--outpath", help="path to saved the parsed document to", default="./data/parsed.pkl")
    parser.add_argument("--parse-stations", action="store_true", help="if set the parsed document is a stations xml, else it is a mesure xml")
    parser.add_argument("--stations-path", help="path of a previously parsed staiton file if the parsed document is a mesure xml")
    args = parser.parse_args()
    if args.parse_stations :
        stations = parse_stations(args.path)
        with open(args.outpath,"wb") as f:
            pkl.dump(stations, f)
    else :
        mesures = parse_mesures(args.path, args.stations_path)
        with open(args.outpath,"wb") as f:
            pkl.dump(mesures, f)

