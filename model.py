import folium
import pymongo
from enum import Enum
import logging

logger = logging.getLogger()

class Pollutant(Enum):
    NO2 = 8
    SO2 = 1
    PM10 = 5
    O3 = 7
    NOX = 9
    CO = 10
    H2S = 11
    PM25 = 6001 

class DBClient:

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client["airQmap"]
        self.stations = self.db["stations"]
        if not "stations" in self.db.list_collection_names():
            self.stations.create_index("station_ref", unique=True)
        
        self.mesures = self.db["mesures"]
        if not "mesures" in self.db.list_collection_names():
            self.mesures.create_index("mesure_ref", unique=True)

    def insert_mesures(self, mesures):
        try :
            self.mesures.insert_many(mesures, ordered=False)
        except :
            logger.debug("failed to insert some mesures due to dupplicated references")

    def insert_stations(self, stations):
        try :
            self.stations.insert_many(stations, ordered=False)
        except:
            logger.debug("failed to insert some mesures due to dupplicated references")


    