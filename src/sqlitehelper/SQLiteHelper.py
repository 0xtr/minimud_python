import sqlite3
import os
from enum import Enum, auto
from src.rooms import SpaceClasses, RoomCRUD


class DBTypes(Enum):
    ROOM_DB = auto()
    PLAYER_DB = auto()
    OBJ_DB = auto()


class QueryResult:
    res = []

    def __init__(self, results):
        self.results = results

    def results(self):
        return self.res


class SQLExecution:
    query = ''
    queryArgs = ''
    dbToRunOn = []
    queryResult = None

    def __init__(self, query, queryArgs, dbToRunOn):
        self.query = query
        self.queryArgs = queryArgs
        self.dbToRunOn = dbToRunOn
        self.run()

    def run(self):
        print("sql " + self.query)

        conn = SQLDBConnector.dbConnections[self.dbToRunOn]
        print("conn " + conn)
        assert conn
        cursor = conn.cursor()
        # is it okay if queryargs is empty to do this
        cursor.execute(self.query, self.queryArgs)
        print("results for [" + self.query + "]: " + cursor.fetchall)

        self.queryResult = QueryResult(cursor.fetchall())
        print(QueryResult(cursor.fetchall()))
        return self

    def results(self):
        return self.queryResult


class SQLDBConnector:
    dbLocations = {
        DBTypes.ROOM_DB: "roomdb.db",
        DBTypes.PLAYER_DB: "playerdb.db",
        DBTypes.OBJ_DB: "objdb.db"
    }
    dbConnections = []

    # update with locs
    # CLEAN ME
    def __init__(self):
        tables_needed = True
        for val in list(self.dbLocations.values()):
            print(val)
            if os.path.exists(val) and os.path.isdir(val):
                tables_needed = False
            else:
                if not os.path.exists("dbs"):
                    os.makedirs("dbs")

            self.dbConnections.append(sqlite3.connect(val))

        if tables_needed:
            self.open_objdb()
            self.open_playerdb()
            self.open_roomdb()
            self.insert_base_room()

    def connectedToAllDatabases(self):
        return len(self.dbConnections) == len(self.dbLocations)

    @staticmethod
    def insert_base_room():
        coords = 0, 0, 0
        room = RoomCRUD.lookup_room(coords)
        if room.id > 0:
            return 0

        # check that we have at least the origin room
        rconfig = SpaceClasses.RoomBlueprint()
        rconfig.name = "The Core of the World"
        rconfig.desc = "It is pitch black. You are likely to be eaten by a null character."
        rconfig.coords = [0, 0, 0]
        rconfig.owner = "system"
        rconfig.flags = "none"

        result = RoomCRUD.insert_room(rconfig)
        assert result.id == 1

    @staticmethod
    def open_playerdb():
        queryResult = SQLExecution(
            "CREATE TABLE PLAYERS (id PRIMARY KEY AUTOINCREMENT,"
            "name TEXT, hash TEXT, salt TEXT, last_ip TEXT,"
            "loc_id INT)", {}, DBTypes.PLAYER_DB)

        assert queryResult.results() is not None

    @staticmethod
    def open_objdb():
        queryResult = SQLExecution(
            "CREATE TABLE OBJECTS (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "obj_name TEXT, obj_keywords TEXT, obj_desc TEXT, obj_createdby TEXT,"
            " obj_location INT, obj_playerid INT)", {}, DBTypes.OBJ_DB)

        assert queryResult.results() is not None

    @staticmethod
    def open_roomdb():
        queryResult = SQLExecution(
            "CREATE TABLE ROOMS (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name TEXT, desc TEXT, "
            "x INT, y INT, z  INT,"
            "north INT, east INT, south INT,"
            "west  INT, up   INT, down  INT,"
            "northeast INT, southeast INT, southwest INT," "northwest INT,"
            "owner TEXT, last_modified_by TEXT,"
            "flags TEXT)", {}, DBTypes.ROOM_DB)

        assert queryResult.results() is not None
