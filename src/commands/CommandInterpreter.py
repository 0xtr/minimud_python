from src.commands.CommandClasses import CommandTypes, get_command_info
from src.commands.CommandExecutor import do_cmd_action
from src.io.IncomingHandler import check_if_name_is_valid, \
    check_if_name_is_reserved, check_if_player_is_already_online, \
    handle_existing_pass, set_player_confirm_new_pw, handle_new_pass
from src.io.OutputBuilder import print_to_player, PrintArg, print_room_to_player
from src.players.PlayerCRUD import ensure_player_moving_valid_dir, lookup_player
from src.players.PlayerManagementLive import reset_player_state, \
    PlayerWaitStates
from src.players.PlayerMovement import calc_coords_from_playerloc_and_dir
from src.rooms import SpaceClasses
from src.rooms.RoomCRUD import adjust_room_desc, lookup_room, adjust_room_name, \
    insert_room, link_rooms, remove_room, compare_room_owner
from src.rooms.SpaceClasses import RoomBlueprint


def interpret_command(player):
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
        print("Unhandled wait state " + player.wait_state + " on player " + player.name)

    return 0


def alter_room_links(player, command):
    if (ensure_player_moving_valid_dir(player, command)) == SpaceClasses.EXIT_FAILURE:
        reset_player_state(player)
        return 1

    dest_coords = calc_coords_from_playerloc_and_dir(player)
    src_room = lookup_room(player.coords)
    dest_room = lookup_room(dest_coords)

    if dest_room is None:
        print_to_player(player, PrintArg.PRINT_COULDNT_EXIT_NO_ROOM)

    if compare_room_owner(player, player.coords) == 1:
        print_to_player(player, PrintArg.PRINT_INSUFFICIENT_PERMISSIONS)

    info = get_command_info(command)
    rv = link_rooms(info.subtype, src_room, dest_room)

    if rv == 0:
        print_to_player(player, PrintArg.PRINT_TOGGLED_ROOM_EXIT)
    elif rv == 1:
        print_to_player(player, PrintArg.PRINT_COULDNT_TOGGLE_EXIT)

    reset_player_state(player)


def alter_room_desc(player, command):
    if command is not None and command[0] is not 'y':
        print_to_player(player, PrintArg.PRINT_EXITING_CMD_WAIT)
        reset_player_state(player)

    result = adjust_room_desc(player)
    if result == 0:
        print_to_player(player, PrintArg.PRINT_ADJUSTMENT_SUCCESSFUL)
    elif result is 1:
        print_to_player(player, PrintArg.PRINT_COULDNT_ADJUST_ROOM)
    elif result is 2:
        print_to_player(player, PrintArg.PRINT_INSUFFICIENT_PERMISSIONS)

    reset_player_state(player)
    roomResult = lookup_room(player.coords)
    print_room_to_player(player, roomResult)


def alter_room_name(player, command):
    if command is not None and command[0] is not 'y':
        print_to_player(player, PrintArg.PRINT_EXITING_CMD_WAIT)
        reset_player_state(player)

    result = adjust_room_name(player)
    if result == 0:
        print_to_player(player, PrintArg.PRINT_ADJUSTMENT_SUCCESSFUL)
    elif result == 1:
        print_to_player(player, PrintArg.PRINT_COULDNT_ADJUST_ROOM)
    elif result == 2:
        print_to_player(player, PrintArg.PRINT_INSUFFICIENT_PERMISSIONS)

    reset_player_state(player)
    roomResult = lookup_room(player.coords)
    print_room_to_player(player, roomResult)


def handle_room_creation(player, command):
    if command is not None and command[0] is not 'y':
        print_to_player(player, PrintArg.PRINT_EXITING_CMD_WAIT)
        reset_player_state(player)

    dest_coords = calc_coords_from_playerloc_and_dir(player)
    roomResult = lookup_room(dest_coords)

    if roomResult.id > 0:
        print_to_player(player, PrintArg.PRINT_ROOM_ALREADY_EXISTS)
        reset_player_state(player)
        return

    #check here for their perms
    #print_to_player(player, PRINT_INSUFFICIENT_PERMISSIONS)

    rconfig = RoomBlueprint()
    rconfig.name = "NULL SPACE"
    rconfig.coords = dest_coords
    rconfig.desc = "It is pitch black. You are likely to be eaten by a null character."
    rconfig.owner = player.name
    rconfig.flags = "none"

    existing = lookup_room(player.coords)
    new = insert_room(rconfig)

    if new is None:
        print_to_player(player, PrintArg.PRINT_ROOM_CREATION_FAILURE)
        return

    print_to_player(player, PrintArg.PRINT_ROOM_CREATION_SUCCESS)

    info = get_command_info(player.store)
    link_rooms(info.subtype, existing, new)

    existing = lookup_room(player.coords)
    print_room_to_player(player, existing)
    reset_player_state(player)


def handle_room_removal(player, command):
    if command is not None and command[0] is not 'y':
        print_to_player(player, PrintArg.PRINT_EXITING_CMD_WAIT)
        reset_player_state(player)

    # TODO: check exits etc handled & players in room moved
    result = remove_room(player)
    if result == 0:
        print_to_player(player, PrintArg.PRINT_ROOM_REMOVAL_SUCCESS)
    elif result == -1:
        print_to_player(player, PrintArg.PRINT_ROOM_REMOVAL_FAILURE)
    elif result == -2:
        print_to_player(player, PrintArg.PRINT_INSUFFICIENT_PERMISSIONS)

    reset_player_state(player)


def handle_incoming_name(player, command):
    if check_if_name_is_valid(player, command) is False:
        return False
    if check_if_name_is_reserved(player, command) is True:
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


def prepare_for_new_room_desc(player, command):
    player.store = command
    player.wait_state = PlayerWaitStates.WAIT_CONFIRM_NEW_ROOM_DESC
    print_to_player(player, PrintArg.PRINT_CONFIRM_NEW_ROOM_DESC)


def prepare_for_new_room_name(player, command):
    player.store = command
    player.wait_state = PlayerWaitStates.WAIT_CONFIRM_NEW_ROOM_NAME
    print_to_player(player, PrintArg.PRINT_CONFIRM_NEW_ROOM_NAME)


def prepare_for_room_mk(player, command):
    if ensure_player_moving_valid_dir(player, command) is 1:
        reset_player_state(player)
        return

    player.store = command
    player.wait_state = PlayerWaitStates.WAIT_ROOM_CREATION_CONF

    print_to_player(player, PrintArg.PRINT_ROOM_CREATION_CONFIRMALL)


def prepare_for_room_rm(player):
    print_to_player(player, PrintArg.PRINT_ROOM_REMOVAL_CONFIRM)
    player.wait_state = PlayerWaitStates.WAIT_ROOM_REMOVAL_CONFIRM
