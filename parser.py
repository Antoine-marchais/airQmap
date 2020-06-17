from bs4 import BeautifulSoup
import pickle as pkl
import argparse
import logging
from model import Pollutant, DBClient
import datetime as dt

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
        station["station_ref"] = elt["gml:id"].split("-")[-1]
        station["position"] = [float(coord) for coord in elt.find("gml:pos").string.split()]
        stations.append(station)
    return stations

def parse_mesures(last_mesures_xml):
    """
    Parse a mesure xml using the previously parsed stations

    Args:
         last_mesures_xml (string): xml string containing the last mesures

    Returns:
        list(dict): list of mesures with the geographical coordinates of mesure points
    """
    dbclient = DBClient("localhost")

    soup = BeautifulSoup(last_mesures_xml, "xml")
    elts = soup.find_all("om:OM_Observation")
    mesures = []
    for elt in elts :
        mesure_batch = []
        try :
            values = elt.find("swe:values").string.split("@@")[:-1]
            for i, value in enumerate(values) : 
                mesure = {}
                mesure["mesure_ref"] = elt["gml:id"]+"_"+str(i)
                mesure["start_mesure"] = dt.datetime.fromisoformat(value.split(",")[0]).astimezone()
                mesure["end_mesure"] = dt.datetime.fromisoformat(value.split(",")[1]).astimezone()
                mesure["value"] = float(value.split(",")[4])
                mesure["station_id"] = elt.find("om:name",{"xlink:href":"http://dd.eionet.europa.eu/vocabulary/aq/processparameter/SamplingPoint"}).find_next()["xlink:href"]
                pollutant_idx = int(elt.find("om:observedProperty")["xlink:href"].split("/")[-1])
                mesure["pollutant"] = Pollutant(pollutant_idx).name
                mesure["position"] = {}
                station_id = mesure["station_id"].split("/")[-1].split("-")[-1]
                position = get_station_coords(station_id, dbclient)
                mesure["position"]["x"] = position[0]
                mesure["position"]["y"] = position[1]
                mesure_batch.append(mesure)
            mesures += mesure_batch
        except :
            logger.debug(f"unable to parse the following element :\n {elt.prettify()}")
    return mesures

def get_station_coords(station_id, dbclient):
    """find the station coordinates using its id

    Args:
        station_id (string): id of the station
        stations_df (DBClient): database client of all stations

    Returns:
        [int, int]: latitude and longitude of the station
    """
    return dbclient.stations.find_one({"station_ref":station_id})["position"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path of the document to parse")
    parser.add_argument("--parse-stations", action="store_true", help="if set the parsed document is a stations xml, else it is a mesure xml")
    args = parser.parse_args()
    client = DBClient("localhost")
    if args.parse_stations :
        with open(args.path,"r") as f:
            stations_xml = f.read()
        stations = parse_stations(stations_xml)
        client.insert_stations(stations)
    else :
        mesures = parse_mesures(args.path)
        client.insert_mesures(mesures)

