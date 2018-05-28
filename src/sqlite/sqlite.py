import sqlite3
import os
import sys

ROOM_DB_TYPE    = -1
PLAYER_DB_TYPE  = -2
OBJ_DB_TYPE     = -3

conn = ''

def players_in_room(r_id):
    uint8_t r_id_str[2 * sizeof(r_id)] = {0}
    snprint((char *)r_id_str, sizeof(r_id), "%d", r_id)

    struct query_matches *matches = init_query()
    int32_t rv = run_sql(
        sqlite3_mprint("SELECT id FROM PLAYERS WHERE loc_id = %Q",
                        r_id_str), matches, DB_PLAYER_COUNT)
    assert(rv == 0)
    return matches

def query_matches:
    return (struct query_matches *)calloc(sizeof(struct query_matches), sizeof(struct query_matches))

def add_query_match(qmatches, id):
    ++qmatches->matches
    qmatches->ids = realloc(qmatches->ids, sizeof(qmatches->ids) + sizeof(int32_t))
    qmatches->ids[(qmatches->matches-1)] = atoi(id)

    for (size_t i = 0 i < qmatches->matches; ++i) {
        print "%d ", qmatches->ids[i]
    }
    print "\n"

class QueryMatch:
    matches = ''
    ids = []

    def set(self, matches, ids):
        self.matches = matches
        self.ids = ids

    def matches(self):
        return matches,ids

class SQLExecution:
    def run(self, query, data, type)
        print("sql: %s\n", query)

        if (type == DB_ROOM || type == DB_ROOM_COUNT)
            db = get_roomdb()
        if (type == DB_PLAYER || type == DB_PLAYER_COUNT)
            db = get_playerdb()
        if (type == DB_OBJECT || type == DB_OBJECT_COUNT)
            db = get_objdb()

        if (type == DB_ROOM)
            func = room_callback
        if (type == DB_PLAYER)
            func = player_callback
        if (type == DB_PLAYER_COUNT || type == DB_ROOM_COUNT)
            func = count_callback

        assert(db != NULL)

        if (sqlite3_exec(db, query, func, data, (char **)sqlerr) != SQLITE_OK) {
            fprint(stdout, "sqlite error:\n%s\n", sqlite3_errmsg(db))
            sqlite3_free(query)
            sqlite3_free(sqlerr)
            return EXIT_FAILURE

        sqlite3_free(query)

        return EXIT_SUCCESS

class SQLDBSetup:
    def get_roomdb(self):
        return roomdb

    def set_roomdb(db):
        roomdb = db

    def get_playerdb(self):
        return playerdb

    def set_playerdb(db):
        playerdb = db

    def get_objdb(self):
        return objdb

    def set_objdb(db):
        objdb = db

 handle_player_columns(char *azColName, char *arg1, struct player_db_record *player)
 handle_map_columns(char *azColName, char *arg1, struct room_db_record *map)

def room_callback(data, argc, argv, azColName):
    struct room_db_record *map_ref = data

    increment_sqlite_rows_count()

    if (data == NULL)
        return EXIT_SUCCESS

    memset(map_ref->exits, -1, sizeof(map_ref))
    map_ref->found = true

    for (size_t i = 0 i < (size_t)argc; ++i)
    handle_map_columns(azColName[i], argv[i], map_ref)

    return EXIT_SUCCESS

def count_callback(data, argc, argv, azColName):
    struct query_matches *qmatches = data

    for (size_t i = 0 i < (size_t)argc; ++i) {
        if (memcmp(azColName[i], "id", strlen(azColName[i])) != 0)
            continue

        add_query_match(qmatches, argv[i])
        break
    }

    return EXIT_SUCCESS

def player_callback (data, argc, argv, azColName):
    struct player_db_record *player_ref = data

    increment_sqlite_rows_count()

    if (data == NULL)
        return EXIT_SUCCESS

    for (size_t i = 0 i < (size_t)argc; ++i)
    handle_player_columns(azColName[i], argv[i], player_ref)

    return EXIT_SUCCESS

def handle_player_columns(azColName, arg1, player):
    arg_len = strlen(arg1)
    col_len = strlen(azColName)

    if (memcmp(azColName, "loc_id", col_len) == 0) {
    player->loc_id = atoi(arg1)
    } else if (memcmp(azColName, "hash", col_len) == 0) {
    memcpy(player->hash, arg1, arg_len)
    } else if (memcmp(azColName, "name", col_len) == 0) {
    memcpy(player->name, arg1, arg_len)
    } else if (memcmp(azColName, "salt", col_len) == 0) {
    memcpy(player->salt, arg1, arg_len)
    } else if (memcmp(azColName, "last_ip", col_len) == 0) {
    memcpy(player->last_ip, arg1, arg_len)
    } else if (memcmp(azColName, "id", col_len) == 0) {
    player->id = atoi(arg1)
    }

def handle_map_columns(azColName, rg1, map):
    arg_len = (arg1 != NULL) ? strlen(arg1) : 0
    col_len = strlen(azColName)

    if (memcmp(azColName, "name", col_len) == 0) {
    memcpy(map->rname, arg1, arg_len)
    } else if (memcmp(azColName, "desc", col_len) == 0) {
    memcpy(map->rdesc, arg1, arg_len)
    } else if (memcmp(azColName, "north", col_len) == 0) {
    map->exits[NORTH_EXIT] = atoi(arg1)
    } else if (memcmp(azColName, "east", col_len) == 0) {
    map->exits[EAST_EXIT] = atoi(arg1)
    } else if (memcmp(azColName, "south", col_len) == 0) {
    map->exits[SOUTH_EXIT] = atoi(arg1)
    } else if (memcmp(azColName, "west", col_len) == 0) {
    map->exits[WEST_EXIT] = atoi(arg1)
    } else if (memcmp(azColName, "up", col_len) == 0) {
    map->exits[UP_EXIT] = atoi(arg1)
    } else if (memcmp(azColName, "down", col_len) == 0) {
    map->exits[DOWN_EXIT] = atoi(arg1)
    } else if (memcmp(azColName, "northeast", col_len) == 0) {
    map->exits[NORTHEAST_EXIT] = atoi(arg1)
    } else if (memcmp(azColName, "southeast", col_len) == 0) {
    map->exits[SOUTHEAST_EXIT] = atoi(arg1)
    } else if (memcmp(azColName, "southwest", col_len) == 0) {
    map->exits[SOUTHWEST_EXIT] = atoi(arg1)
    } else if (memcmp(azColName, "northwest", col_len) == 0) {
    map->exits[NORTHWEST_EXIT] = atoi(arg1)
    } else if (memcmp(azColName, "owner", col_len) == 0) {
    memcpy(map->owner, arg1, arg_len)
    } else if (memcmp(azColName, "id", col_len) == 0) {
    map->id = atoi(arg1)
    } else if (memcmp(azColName, "x", col_len) == 0) {
    map->coords.x = atoi(arg1)
    } else if (memcmp(azColName, "y", col_len) == 0) {
    map->coords.y = atoi(arg1)
    } else if (memcmp(azColName, "z", col_len) == 0) {
    map->coords.z = atoi(arg1)
    }

static int rows_count
int32_t get_sqlite_rows_count(void)
{
return rows_count
}
void increment_sqlite_rows_count(void)
{
++rows_count
}
void set_sqlite_rows_count(const int32_t newval)
{
rows_count = newval
}
void reset_sqlite_rows_count(void)
{
rows_count = 0
}

class SQLDBManager:
    def open(self, type, loc):
        tables_needed = False

        if os.path.exists(loc) & os.path.isdir(loc):
            tables_needed = True
        else:
            os.makedir("dbs")

        conn = sqlite3.connect(loc)
        assert conn

        if (tables_needed):
            self.create_player_table()
            self.create_obj_table()
            self.create_room_table()
            self.insert_base_room()

        return sys.EXIT_SUCCESS

    def insert_base_room(self):
        coords = 0, 0, 0

        room = rooms.lookup_room(coords)
        if room.id > 0:
            return sys.EXIT_SUCCESS

        # check that we have at least the origin room
        rconfig = RoomConfig()
        rconfig.name = "The Core of the World"
        rconfig.desc = "It is pitch black. You are likely to be eaten by a null character."
        rconfig.coords.x = 0
        rconfig.coords.y = 0
        rconfig.coords.z = 0
        rconfig.owner = "system"
        rconfig.flags = "none"

        result = rooms.insert_room(rconfig)
        assert(result.id == 1)

    def open_playerdb(self):
        assert(run_sql(sqlite3_mprint(
            "CREATE TABLE PLAYERS (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name TEXT, hash TEXT, salt TEXT, last_ip TEXT,"
            "loc_id INT)"), 0, DB_PLAYER) == EXIT_SUCCESS)

    def open_objdb(self):
        assert(run_sql(sqlite3_mprint(
            "CREATE TABLE OBJECTS (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "obj_name TEXT, obj_keywords TEXT, obj_desc TEXT, obj_createdby TEXT,"
            "obj_location INT, obj_playerid INT)"), 0, DB_OBJECT) == EXIT_SUCCESS)

    def open_roomdb(self):
        assert(run_sql(sqlite3_mprint(
            "CREATE TABLE ROOMS (id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "name TEXT, desc TEXT, "
            "x INT, y INT, z  INT,"
            "north INT, east INT, south INT,"
            "west  INT, up   INT, down  INT,"
            "northeast INT, southeast INT, southwest INT," "northwest INT,"
            "owner TEXT, last_modified_by TEXT,"
            "flags TEXT)"), 0, DB_ROOM) == 0)
