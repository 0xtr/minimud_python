import sqlite3
import os
from enum import Enum, auto
from src.rooms import SpaceClasses, RoomCRUD


class DBTypes(Enum):
    ROOM_DB = auto()
    PLAYER_DB = auto()
    OBJ_DB = auto()
    # move to sql manager
    dbLocations = {
        ROOM_DB, "roomdb.db",
        PLAYER_DB, "playerdb.db",
        OBJ_DB, "objdb.db"
    }


class QueryResult:
    results = []

    def __init__(self, results):
        self.results = results


class SQLExecution:
    query = ''
    queryArgs = ''
    dbToRunOn = []

    def __init__(self, query, queryArgs, dbToRunOn):
        self.query = query
        self.queryArgs = queryArgs
        self.dbToRunOn = dbToRunOn

    def run(self, data):
        print("sql " + self.query)

        conn = SQLDBManager.dbConnections[self.dbToRunOn]
        print("conn " + conn)
        assert conn
        cursor = conn.cursor()
        # is it okay if queryargs is empty to do this
        cursor.execute(self.query, self.queryArgs)
        print("results for [" + self.query + "]: " + cursor.fetchall);

        return QueryResult(cursor.fetchall())


class SQLDBManager:
    dbConnections = {}

    # update with locs
    # CLEAN ME
    def __init__(self, type, loc):
        for i in len(DBTypes.dbLocations):
            self.dbConnections.add(sqlite3.connect(DBTypes.dbLocations[i]))

        tables_needed = False

        if os.path.exists(loc) and os.path.isdir(loc):
            tables_needed = True
        else:
            os.makedir("dbs")

        conn = sqlite3.connect(loc)
        assert conn

        if tables_needed:
            self.create_player_table()
            self.create_obj_table()
            self.create_room_table()
            self.insert_base_room()

        return 0

    def insert_base_room(self):
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

    def open_playerdb(self):
        assert (run_sql(sqlite3_mprint(
            "CREATE TABLE PLAYERS (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name TEXT, hash TEXT, salt TEXT, last_ip TEXT,"
            "loc_id INT)"), 0, DB_PLAYER) == EXIT_SUCCESS)

    def open_objdb(self):
        assert (run_sql(sqlite3_mprint(
            "CREATE TABLE OBJECTS (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "obj_name TEXT, obj_keywords TEXT, obj_desc TEXT, obj_createdby TEXT,"
            "obj_location INT, obj_playerid INT)"), 0,
            DB_OBJECT) == EXIT_SUCCESS)

    def open_roomdb(self):
        assert (run_sql(sqlite3_mprint(
            "CREATE TABLE ROOMS (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name TEXT, desc TEXT, "
            "x INT, y INT, z  INT,"
            "north INT, east INT, south INT,"
            "west  INT, up   INT, down  INT,"
            "northeast INT, southeast INT, southwest INT," "northwest INT,"
            "owner TEXT, last_modified_by TEXT,"
            "flags TEXT)"), 0, DB_ROOM) == 0)
