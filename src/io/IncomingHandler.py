from src.io.CommandInterpreter import CommandTypes, get_command_info
from src.io.IODefs import IODefs

from src.players.PlayerManagement import PlayerWaitStates, \
    get_player, shutdown_socket, \
    handle_new_pass, set_player_confirm_new_pw, handle_existing_pass, \
    handle_incoming_name
from src.players.PlayerMovement import do_movement_cmd, do_travel_cmd

from src.rooms.RoomCRUD import alter_room_links, handle_room_creation, \
    handle_room_removal, alter_room_name, alter_room_desc, prepare_for_room_mk, \
    prepare_for_room_rm, prepare_for_new_room_desc, prepare_for_new_room_name, \
    do_room_cmd


def incoming_handler(socket):
    bufLenMax = IODefs.BUFFER_LENGTH.value
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


def do_system_cmd(player, info):
    if info.subtype == SystemAction.SYS_SAY:
        print_player_speech(player)
    elif info.subtype == SystemAction.SYS_QUIT:
        shutdown_socket(player)


def interpret_command(player):
    printActions = []

    command = player.buffer.lower()
    print("player command: " + command)
    commandInfo = get_command_info(command)

    if player.holding_for_input is False:
        if commandInfo.type == CommandTypes.COMMAND_NOT:
            print_to_player(player, PrintArg.INVALCMD)
            return 1

        return do_cmd_action(player, commandInfo.info)

    # should probably handle 'quit' if they want to exit this process, or C - C
    if player.wait_state == PlayerWaitStates.THEIR_NAME:
        handle_incoming_name(player, command)
    elif player.wait_state == PlayerWaitStates.THEIR_PASSWORD:
        handle_existing_pass(player, command)
    elif player.wait_state == PlayerWaitStates.THEIR_PASSWORD_NEWPRELIM:
        set_player_confirm_new_pw(player, command)
    elif player.wait_state == PlayerWaitStates.THEIR_PASSWORD_NEWFINAL:
        handle_new_pass(player, command)
    elif player.wait_state == PlayerWaitStates.WAIT_ENTER_NEW_ROOM_NAME:
        prepare_for_new_room_name(player, command)
    elif player.wait_state == PlayerWaitStates.WAIT_CONFIRM_NEW_ROOM_NAME:
        alter_room_name(player, command)
    elif player.wait_state == PlayerWaitStates.WAIT_ENTER_NEW_ROOM_DESC:
        prepare_for_new_room_desc(player, command)
    elif player.wait_state == PlayerWaitStates.WAIT_CONFIRM_NEW_ROOM_DESC:
        alter_room_desc(player, command)
    elif player.wait_state == PlayerWaitStates.WAIT_ROOM_REMOVAL_CHECK:
        prepare_for_room_rm(player)
    elif player.wait_state == PlayerWaitStates.WAIT_ROOM_REMOVAL_CONFIRM:
        handle_room_removal(player, command)
    elif player.wait_state == PlayerWaitStates.WAIT_ROOM_CREATION_DIR:
        prepare_for_room_mk(player, command)
    elif player.wait_state == PlayerWaitStates.WAIT_ROOM_CREATION_CONF:
        handle_room_creation(player, command)
    elif player.wait_state == PlayerWaitStates.WAIT_ENTER_FLAG_NAME:
        print("dead code")
    elif player.wait_state == PlayerWaitStates.WAIT_ENTER_EXIT_NAME:
        alter_room_links(player, command)
    else:
        print(
            "Unhandled wait state " + player.wait_state + " on player " + player.name)

    return printActions
