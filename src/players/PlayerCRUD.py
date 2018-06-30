import os
import bcrypt
from src.io import OutputBuilder
from src.players import PlayerManagementLive
from src.commands import CommandClasses
from src.sqlitehelper import SQLiteHelper


class PlayerDBRecord:
    name = ''
    ourHash = ''
    salt = ''
    last_ip = ''
    id = -1
    loc_id = -1


def get_player_coords(player):
    queryResult = SQLiteHelper.SQLExecution(
        "SELECT * FROM PLAYERS WHERE name = :name",
        {"name": player.name},
        SQLiteHelper.DBTypes.PLAYER_DB)
    # room_db_record = SpaceClasses.lookupRoomById(player_db_record.loc_id)
    # return room_db_record.coordinates
    # fixme
    return queryResult.result


# merge the two into just get_player_room
def get_player_loc_id(player):
    queryResult = SQLiteHelper.SQLExecution(
        "SELECT * FROM PLAYERS WHERE name = :name",
        {"name": player.name},
        SQLiteHelper.DBTypes.PLAYER_DB)
    return queryResult.results


def insert_player(player, pw):
    salt = os.urandom(50)
    hashed = bcrypt.hashpw(pw, salt)

    queryResult = SQLiteHelper.SQLExecution(
        "INSERT INTO PLAYERS (name, hash, salt, last_ip, loc_id) VALUES ("
        ":name,:hash,:salt,:last_ip,:loc_id)",
        {"name": player.name, "hash": hashed, "salt": salt, "last_ip": "-",
         "loc_id": 0},
        SQLiteHelper.DBTypes.PLAYER_DB)

    if len(queryResult.results) == 0:
        return 1

    OutputBuilder.print_to_player(player,
                                  OutputBuilder.PrintArg.PLAYER_CREATION_SUCCESS)

    return 0


def lookup_player(name):
    player = PlayerDBRecord()
    queryResult = SQLiteHelper.SQLExecution(
        "SELECT * FROM PLAYERS WHERE name = :name",
        {"name": name},
        SQLiteHelper.DBTypes.PLAYER_DB)

    if queryResult.results.id == -1:
        return None

    return player


def adjust_player_location(player, room_id):
    return SQLiteHelper.SQLExecution(
        "UPDATE PLAYERS SET loc_id =:room_id WHERE name =:pname",
        {"loc_id": room_id, "name": player.name},
        SQLiteHelper.DBTypes.PLAYER_DB)


def ensure_player_moving_valid_dir(player, command):
    command = CommandClasses.categorize_command(command)

    if command.type == CommandClasses.Movement:
        return 0

    OutputBuilder.print_to_player(player,
                                  OutputBuilder.PrintArg.PRINT_INVAL_DIR)
    OutputBuilder.print_to_player(player,
                                  OutputBuilder.PrintArg.PRINT_EXITING_CMD_WAIT)

    PlayerManagementLive.reset_player_state(player)

    return 1


def players_in_room(r_id):
    return SQLiteHelper.SQLExecution(
        "SELECT id FROM PLAYERS WHERE loc_id =:rid",
        {"rid": r_id},
        SQLiteHelper.DBTypes.PLAYER_DB)
