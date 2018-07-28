import os

import bcrypt

from src.io import CommandInterpreter
from src.io.IODefs import IODefs
from src.io.OutputBuilder import print_to_player, print_room_to_player
from src.io.PrintArg import PrintArg
from src.players.ActivePlayers import ActivePlayers

from src.players.PlayerDBRecord import PlayerDBRecord
from src.players.PlayerLiveRecord import PlayerLiveRecord
from src.players.PlayerMovement import adjust_player_location
from src.players.PlayerWaitStates import PlayerWaitStates
from src.rooms.RoomCRUD import lookup_room, lookup_room_by_id
from src.sqlitehelper import SQLiteHelper


def get_player(socket):
    for player in ActivePlayers.activePlayers:
        if player.socket == socket:
            return player

    return None


def get_player_by_id(pid):
    for player in ActivePlayers.activePlayers:
        if player.db_id == pid:
            return player

    return None


def remove_player_by_socket(socket):
    print("remove by socket ", socket)
    ActivePlayers.activePlayers.remove(get_player(socket))
    # remove from select socklist?


def add_new_player(socket):
    player = PlayerLiveRecord()
    player.db_id = -1
    player.socket = socket
    player.holding_for_input = True
    player.wait_state = PlayerWaitStates.THEIR_NAME
    ActivePlayers.activePlayers.append(player)


def get_num_of_players():
    return len(ActivePlayers.activePlayers)


def reset_player_state(player):
    player.wait_state = PlayerWaitStates.NO_WAIT_STATE
    player.holding_for_input = False
    player.store = ''


def check_for_highest_socket_num():
    sock_max = 0
    for player in ActivePlayers.activePlayers:
        if player.socket_num > sock_max:
            sock_max = player.socket_num

    return sock_max


def shutdown_socket(player):
    player.socket.shutdown(player.socket.SHUT_RDWR)
    player.socket.close()
    remove_player_by_socket(player.socket_num)
    return 0


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
    from src.io.OutputBuilder import print_to_player, PrintArg

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

    print_to_player(player, PrintArg.PLAYER_CREATION_SUCCESS)

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


def ensure_player_moving_valid_dir(player, command):
    from src.io.OutputBuilder import print_to_player, PrintArg
    if command.type == CommandInterpreter.Movement:
        return 0
    print_to_player(player, PrintArg.PRINT_INVAL_DIR)
    print_to_player(player, PrintArg.PRINT_EXITING_CMD_WAIT)

    reset_player_state(player)

    return 1


def players_in_room(r_id):
    return SQLiteHelper.SQLExecution(
        "SELECT id FROM PLAYERS WHERE loc_id =:rid",
        {"rid": r_id},
        SQLiteHelper.DBTypes.PLAYER_DB)


def check_player_pass(player, pw):
    # TODO: do this and pass to insert_player
    # what did past me even mean with that comment
    buf_len = IODefs.BUFFER_LENGTH.value
    PASSWORD_LEN = buf_len if (len(pw) > buf_len) else len(pw)

    if PASSWORD_LEN <= 1:
        return 1

    salt_and_pw = player.salt + pw
    if not bcrypt.checkpw(salt_and_pw, player.hash):
        return 1
    else:
        return 0


def handle_existing_pass(player, command):
    player_db = lookup_player(player.name)

    if player_db is None:
        print_to_player(player, PrintArg.UNABLE_TO_RETRIEVE_CHAR)
        player.wait_state = PlayerWaitStates.THEIR_NAME
        return 1

    pid = player_db.id
    # clear pnames if this fails, cause failures are being logged
    # again, what
    if not check_player_pass(player_db, command):
        print_to_player(player, PrintArg.INCORRECT_PASSWORD)
        player.name = ''
        player.wait_state = PlayerWaitStates.THEIR_NAME
        return 1

    roomResult = lookup_room(player.coords)

    if roomResult is None:
        assert adjust_player_location(player, 0) == 0

    player.id = pid
    print_room_to_player(player, roomResult)

    reset_player_state(player)
    player.connected = True

    print("Player name " + player.name + " connected on socket " + str(
        player.socket_num))
    return 0


def handle_new_pass(player, command):
    from src.io.OutputBuilder import print_to_player, PrintArg, print_room_to_player
    if command != player.store or len(command) != len(player.store):
        print_to_player(player, PrintArg.MISMATCH_PW_SET)

        player.wait_state = PlayerWaitStates.THEIR_NAME
        player.store = ''
        return 1

    print_to_player(player, PrintArg.ATTEMPT_CREATE_USR)

    if insert_player(player, command) == -1:
        print_to_player(player, PrintArg.PLAYER_CREATION_FAILED)
        shutdown_socket(player)
        return 1

    reset_player_state(player)
    roomResult = lookup_room_by_id(0)
    print_room_to_player(player, roomResult)

    print("Player name " + player.name + " connected on socket " + str(
        player.socket_num))
    return 0


def set_player_confirm_new_pw(player, command):
    from src.io.OutputBuilder import print_to_player, PrintArg
    player.store = command
    print_to_player(player, PrintArg.REQUEST_PW_CONFIRM)
    player.wait_state = PlayerWaitStates.THEIR_PASSWORD_NEWFINAL
    return 0


def handle_incoming_name(player, command):
    from src.io.OutputBuilder import print_to_player, PrintArg
    if check_if_name_is_valid(player, command) is False:
        return False
    if check_if_name_is_reserved(command) is True:
        return False
    if check_if_player_is_already_online(player, command) is True:
        return False

    player.name = command
    plookup = lookup_player(player.name)

    if plookup is not None:
        print_to_player(player, PrintArg.REQUEST_PW_FOR_EXISTING)
        player.wait_state = PlayerWaitStates.THEIR_PASSWORD_EXISTING
    else:
        print_to_player(player, PrintArg.REQUEST_PW_FOR_NEW)
        player.wait_state = PlayerWaitStates.THEIR_PASSWORD_NEWPRELIM

    return True


def check_if_name_is_reserved(name):
    from src.io.OutputBuilder import PrintArg
    commandList = CommandInterpreter.get_all_commands_as_strings()
    for i in commandList:
        if commandList[i] == name:
            return True, PrintArg.PRINT_NAME_UNAVAILABLE

    return False


def check_if_name_is_valid(player, name):
    from src.io.OutputBuilder import PrintArg
    if len(name) > IODefs.PRINT_LINE_WIDTH.value or len(
            name) < IODefs.NAMES_MIN.value:
        return False, PrintArg.PRINT_NAME_NOT_WITHIN_PARAMS

    for i in player.buffer:
        c = player.buffer[i]
        if c == 0:
            break

        if not c.isalnum() and c != ' ':
            return False, PrintArg.PRINT_NAME_NOT_WITHIN_PARAMS

    return True


def check_if_player_is_already_online(player, name):
    from src.io.OutputBuilder import PrintArg, print_to_player
    playersList = ActivePlayers.activePlayers
    print("num of players on: " + str(playersList.__len__()))

    for i in playersList:
        if name != i.name:
            continue

        print_to_player(player, PrintArg.PLAYER_ALREADY_ONLINE)
        player.wait_state = PlayerWaitStates.THEIR_NAME

        return True, PrintArg.PRINT_PLAYER_ALREADY_ONLINE

    return False


