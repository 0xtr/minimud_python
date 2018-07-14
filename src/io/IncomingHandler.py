from fcntl import ioctl

from src.commands import CommandClasses
from src.commands.CommandInterpreter import interpret_command
from src.io.OutgoingHandler import OutgoingDefs
from src.io.OutputBuilder import print_to_player, PrintArg, print_room_to_player
from src.players.PlayerCRUD import lookup_player, adjust_player_location, \
    insert_player
from src.players.PlayerManagementLive import ActivePlayers, PlayerWaitStates, \
    reset_player_state, get_player, remove_player_by_socket

import bcrypt

from src.rooms.RoomCRUD import lookup_room, lookup_room_by_id


def check_for_highest_socket_num():
    sock_max = 0
    for player in ActivePlayers.activePlayers:
        if player.socket_num > sock_max:
            sock_max = player.socket_num

    return sock_max


def check_player_pass(player, pw):
    # TODO: do this and pass to insert_player
    # what did past me even mean with that comment
    buf_len = OutgoingDefs.BUFFER_LENGTH.value
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
    player.store = command
    print_to_player(player, PrintArg.REQUEST_PW_CONFIRM)
    player.wait_state = PlayerWaitStates.THEIR_PASSWORD_NEWFINAL
    return 0


def check_if_name_is_reserved(player, name):
    commandList = CommandClasses.get_all_commands_as_strings()
    for i in commandList:
        if commandList[i] == name:
            print_to_player(player, PrintArg.NAME_UNAVAILABLE)
            print_to_player(player, PrintArg.NAME_NOT_WITHIN_PARAMS)
            return True

    return False


def check_if_name_is_valid(player, name):
    if len(name) > OutgoingDefs.PRINT_LINE_WIDTH.value or len(
            name) < OutgoingDefs.NAMES_MIN.value:
        print_to_player(player, PrintArg.NAME_NOT_WITHIN_PARAMS)
        return False

    for i in player.buffer:
        c = player.buffer[i]
        if c == 0:
            break

        if not c.isalnum() and c != ' ':
            return False

    return True


def check_if_player_is_already_online(player, name):
    playersList = ActivePlayers.activePlayers
    print("num of players on: " + playersList.__len__())

    for i in playersList.__len__():
        if name != playersList[i].name:
            continue

        print_to_player(player, PrintArg.PLAYER_ALREADY_ONLINE)

        player.wait_state = PlayerWaitStates.THEIR_NAME

        return True

    return False


def incoming_handler(socket):
    bufLenMax = OutgoingDefs.BUFFER_LENGTH.value
    buffer = len(socket.recv(bufLenMax, socket.MSG_PEEK))
    print("peeked: " + str(buffer))
    buffer = socket.recv(bufLenMax, 0)

    while len(socket.recv(bufLenMax, socket.MSG_PEEK)) > 0:
        socket.recv(bufLenMax, 0)

    player = get_player(socket)

    if len(buffer) == 0:
        return shutdown_socket(player)

    player.buffer = buffer

    strip_carriage_returns(player)
    interpret_command(player)

    return 0


def strip_carriage_returns(player):
    for i in range(0, len(player.buffer)):
        if player.buffer[i] == '\r':
            player.buffer[i] = '\0'


def shutdown_socket(player):
    player.socket.shutdown(player.socket.SHUT_RDWR)
    player.socket.close()
    remove_player_by_socket(player.socket_num)
    return 0
