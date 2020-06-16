from bs4 import BeautifulSoup
import pickle as pkl
import argparse

def parse_stations(path_to_stations):
    with open(path_to_stations,"r") as f:
        station_xml = f.read()

    soup = BeautifulSoup(station_xml, "xml")
    print("soupified")
    elts = soup.find_all("gml:Point")
    stations = []
    for elt in elts : 
        station = {}
        station["id"] = elt["gml:id"].split("-")[-1]
        station["position"] = [float(coord) for coord in elt.find("gml:pos").string.split()]
        stations.append(station)
    return stations

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

