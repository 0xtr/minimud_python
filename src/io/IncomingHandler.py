from src.io.CommandInterpreter import CommandTypes, get_command_info, \
    SystemAction, InfoRequest
from src.io.IODefs import IODefs
from src.io.OutputBuilder import print_to_player, print_player_speech, \
    print_room_to_player
from src.io.PrintArg import PrintArg

import src.players.PlayerManagement
from src.players.PlayerMovement import do_movement_cmd, do_travel_cmd

from src.rooms.RoomCRUD import alter_room_links, handle_room_creation, \
    handle_room_removal, alter_room_name, alter_room_desc, prepare_for_room_mk, \
    prepare_for_room_rm, prepare_for_new_room_desc, prepare_for_new_room_name, \
    do_room_cmd, lookup_room


def incoming_handler(socket):
    bufLenMax = IODefs.BUFFER_LENGTH.value
    buffer = socket.recv(bufLenMax)
    print("buffer: [" + str(buffer) + "]")

    # TODO: handle excess data
    #while len(socket.recv(bufLenMax)) > 0:
    #    socket.recv(bufLenMax)

    player = src.players.PlayerManagement.get_player(socket)

    if len(buffer) == 0:
        return shutdown(player)

    player.buffer = buffer

    # TODO: fix stripping
    strip_special_chars(player)
    print("stripped: " + str(player.buffer))
    interpret_command(player)

    return 0


def strip_special_chars(player):
    for i in player.buffer:
        if i is '\r' or '\n':
            i = '\0'


def do_cmd_action(player, info):
    if info.type == CommandTypes.MOVEMENT:
        do_movement_cmd(player, info)

    if info.type == CommandTypes.SYSTEM_ACTION:
        do_system_cmd(player, info)

    if info.type == CommandTypes.ROOM_CHANGE:
        do_room_cmd(player, info)

    if info.type == CommandTypes.TRAVEL_ACTION:
        do_travel_cmd(player, info)

    if info.type == CommandTypes.INFO_REQUEST:
        do_info_cmd(player, info)

    return 0


def do_info_cmd(player, info):
    if info.subtype == InfoRequest.INFO_ROOM:
        roomResult = lookup_room(player.coords)
        print_room_to_player(player, roomResult.results())

    if info.subtype == InfoRequest.INFO_COMMANDS:
        print_to_player(player, PrintArg.PLAYER_SHOW_COMMANDS)
    if info.subtype == InfoRequest.INFO_PLAYERS:
        print_to_player(player, PrintArg.LISTPLAYERS)
    if info.subtype == InfoRequest.INFO_MAP:
        print("ADD ME")


def do_system_cmd(player, info):
    if info.subtype == SystemAction.SYS_SAY:
        print_player_speech(player)
    elif info.subtype == SystemAction.SYS_QUIT:
        shutdown(player)


def interpret_command(player):
    command = player.buffer.lower()
    print("player command: " + str(command))
    commandInfo = get_command_info(command)

    if player.holding_for_input is False:
        if commandInfo.type == CommandTypes.COMMAND_NOT:
            return print_to_player(player, PrintArg.INVALCMD)

        return do_cmd_action(player, commandInfo.info)

    # should probably handle 'quit' if they want to exit this process, or C - C
    if player.wait_state == src.players.PlayerManagement.PlayerWaitStates.THEIR_NAME:
        src.players.PlayerManagement.handle_incoming_name(player, command)
    elif player.wait_state == src.players.PlayerManagement.PlayerWaitStates.THEIR_PASSWORD:
        src.players.PlayerManagement.handle_existing_pass(player, command)
    elif player.wait_state == src.players.PlayerManagement.PlayerWaitStates.THEIR_PASSWORD_NEWPRELIM:
        src.players.PlayerManagement.set_player_confirm_new_pw(player, command)
    elif player.wait_state == src.players.PlayerManagement.PlayerWaitStates.THEIR_PASSWORD_NEWFINAL:
        src.players.PlayerManagement.handle_new_pass(player, command)
    elif player.wait_state == src.players.PlayerManagement.PlayerWaitStates.WAIT_ENTER_NEW_ROOM_NAME:
        prepare_for_new_room_name(player, command)
    elif player.wait_state == src.players.PlayerManagement.PlayerWaitStates.WAIT_CONFIRM_NEW_ROOM_NAME:
        alter_room_name(player, command)
    elif player.wait_state == src.players.PlayerManagement.PlayerWaitStates.WAIT_ENTER_NEW_ROOM_DESC:
        prepare_for_new_room_desc(player, command)
    elif player.wait_state == src.players.PlayerManagement.PlayerWaitStates.WAIT_CONFIRM_NEW_ROOM_DESC:
        alter_room_desc(player, command)
    elif player.wait_state == src.players.PlayerManagement.PlayerWaitStates.WAIT_ROOM_REMOVAL_CHECK:
        prepare_for_room_rm(player)
    elif player.wait_state == src.players.PlayerManagement.PlayerWaitStates.WAIT_ROOM_REMOVAL_CONFIRM:
        handle_room_removal(player, command)
    elif player.wait_state == src.players.PlayerManagement.PlayerWaitStates.WAIT_ROOM_CREATION_DIR:
        prepare_for_room_mk(player, command)
    elif player.wait_state == src.players.PlayerManagement.PlayerWaitStates.WAIT_ROOM_CREATION_CONF:
        handle_room_creation(player, command)
    elif player.wait_state == src.players.PlayerManagement.PlayerWaitStates.WAIT_ENTER_FLAG_NAME:
        print("dead code")
    elif player.wait_state == src.players.PlayerManagement.PlayerWaitStates.WAIT_ENTER_EXIT_NAME:
        alter_room_links(player, command)
    else:
        print(
            "Unhandled wait state " + player.wait_state + " on player " + player.name)

    return 0


def shutdown(player):
    return src.players.PlayerManagement.shutdown_socket(player)
