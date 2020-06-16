import folium
import pymongo
from enum import Enum
import logging
from collections import OrderedDict

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
    """
    Client for connecting to the mongodb database
    """

    def __init__(self):
        """
        Create the connection and collections
        """
        self.client = pymongo.MongoClient("mongodb://localhost:27017")
        self.db = self.client["airQmap"]
        self.stations = self.db["stations"]
        if not "stations" in self.db.list_collection_names():
            self.stations.create_index("station_ref", unique=True)
        
        self.mesures = self.db["mesures"]
        if not "mesures" in self.db.list_collection_names():
            self.mesures.create_index("mesure_ref", unique=True)

    def insert_mesures(self, mesures):
        """
        Insert without dupplicates a list of mesures in the database

        Args:
            mesures (list(dict)): list of mesures to insert
        """
        try :
            self.mesures.insert_many(mesures, ordered=False)
        except :
            logger.debug("failed to insert some mesures due to dupplicated references")

    def insert_stations(self, stations):
        """
        Insert without dupplicates a list of mesurement stations in the database

        Args:
            stations (list(dict)): list of stations with their id and coordinates
        """
        try :
            self.stations.insert_many(stations, ordered=False)
        except:
            logger.debug("failed to insert some mesures due to dupplicated references")

    def get_mesures_by_time(self, pollutant):
        """
        Retrieve mesures from the database for a pollutant, and groups them by the time of mesurement in a chronological order

        Args:
            pollutant (string): name of the pollutant

        Returns:
            OrderedDict: dict with datetimes as keys and mesurement lists as values
        """
        times = sorted(self.mesures.distinct("end_mesure", filter={"pollutant":pollutant}))
        ordered_mesures = OrderedDict()
        for time in times :
            ordered_mesures[time] = list(self.mesures.find({"end_mesure":time,"pollutant":pollutant}))
        return ordered_mesures

    