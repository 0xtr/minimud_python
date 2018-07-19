from enum import Enum, auto
from src.io import OutgoingHandler
from src.io.OutgoingHandler import OutgoingDefs
from src.rooms import SpaceClasses
from src.players import PlayerManagementLive
from src.commands import CommandClasses


class PrintArg(Enum):
    PRINT_INVAL_CMD = auto()
    PRINT_INVAL_DIR = auto()
    PRINT_REQUEST_PW_FOR_NEW = auto()
    PRINT_SHOW_CMDS = auto()
    PRINT_REQUEST_PW_CONFIRM = auto()
    PRINT_REQUEST_PW_FOR_EXISTING = auto()
    PRINT_ATTEMPT_CREATE_USR = auto()
    PRINT_MISMATCH_PW_SET = auto()
    PRINT_PLAYER_CREATION_FAILED = auto()
    PRINT_PLAYER_CREATION_SUCCESS = auto()
    PRINT_PLAYER_ALREADY_ONLINE = auto()
    PRINT_INCORRECT_PASSWORD = auto()
    PRINT_UNABLE_TO_RETRIEVE_CHAR = auto()
    PRINT_NAME_UNAVAILABLE = auto()
    PRINT_ALPHANUM_NAMES_ONLY = auto()
    PRINT_NAME_NOT_WITHIN_PARAMS = auto()
    PRINT_PROVIDE_NEW_ROOM_NAME = auto()
    PRINT_PROVIDE_NEW_ROOM_DESC = auto()
    PRINT_CONFIRM_NEW_ROOM_DESC = auto()
    PRINT_CONFIRM_NEW_ROOM_NAME = auto()
    PRINT_ADJUSTMENT_SUCCESSFUL = auto()
    PRINT_COULDNT_ADJUST_ROOM = auto()
    PRINT_EXITING_CMD_WAIT = auto()
    PRINT_INSUFFICIENT_PERMISSIONS = auto()
    PRINT_ROOM_EXIT_CHANGED = auto()
    PRINT_ROOM_FLAG_CHANGED = auto()
    PRINT_ROOM_REMOVAL_CHECK = auto()
    PRINT_ROOM_REMOVAL_CONFIRM = auto()
    PRINT_ROOM_REMOVAL_SUCCESS = auto()
    PRINT_ROOM_REMOVAL_FAILURE = auto()
    PRINT_ROOM_CREATION_GIVE_DIR = auto()
    PRINT_ROOM_CREATION_CONFIRMALL = auto()
    PRINT_ROOM_CREATION_CANNOT = auto()
    PRINT_ROOM_CREATION_SUCCESS = auto()
    PRINT_ROOM_ALREADY_EXISTS = auto()
    PRINT_ROOM_CREATION_FAILURE = auto()
    PRINT_REMOVED_FROM_ROOM = auto()
    PRINT_PROVIDE_ROOM_EXIT_NAME = auto()
    PRINT_PROVIDE_ROOM_FLAG_NAME = auto()
    PRINT_TOGGLED_ROOM_EXIT = auto()
    PRINT_COULDNT_TOGGLE_EXIT = auto()
    PRINT_COULDNT_EXIT_NO_ROOM = auto()


def print_to_player(player, argument):
    bufLenMax = OutgoingDefs.BUFFER_LENGTH.value
    printLineMax = OutgoingDefs.PRINT_LINE_WIDTH.value
    if argument == PrintArg.PRINT_INVAL_CMD:
        player.buffer = "Invalid command. Type \'commands\'.\n"
    elif argument == PrintArg.SHOW_CMDS:
        print_all_commands(player)
    elif argument == PrintArg.PRINT_INVAL_DIR:
        player.buffer = "Cannot move in that direction. Type 'look' to view room.\n"
    elif argument == PrintArg.REQUEST_PW_FOR_NEW:
        player.buffer = "You've provided the name [" + player.name + "].\n\n"
        player.buffer += "Provide a password less than " + bufLenMax + " characters long.\n\n"
    elif argument == PrintArg.REQUEST_PW_CONFIRM:
        player.buffer = "Confirm your password by typing it out once more.\n"
    elif argument == PrintArg.REQUEST_PW_FOR_EXISTING:
        player.buffer = "Provide your password.\n"
    elif argument == PrintArg.ATTEMPT_CREATE_USR:
        player.buffer = "Attempting to create your character...\n"
    elif argument == PrintArg.MISMATCH_PW_SET:
        player.buffer = "Password mismatch. Start over.\nWhat is your NAME.\n"
    elif argument == PrintArg.PLAYER_CREATION_FAILED:
        player.buffer = "Character creation failed. You should never see this.\n"
    elif argument == PrintArg.PLAYER_CREATION_SUCCESS:
        player.buffer = "Character created. Entering the world...\n"
    elif argument == PrintArg.PLAYER_ALREADY_ONLINE:
        player.buffer = "That player is already connected.\n"
    elif argument == PrintArg.INCORRECT_PASSWORD:
        player.buffer = "Incorrect password. Restarting.\n\nWhat is your NAME.\n"
    elif argument == PrintArg.UNABLE_TO_RETRIEVE_CHAR:
        player.buffer = "Couldn't retrieve your character.\n"
    elif argument == PrintArg.NAME_UNAVAILABLE:
        player.buffer = "That name is unavailable.\n"
    elif argument == PrintArg.ALPHANUM_NAMES_ONLY:
        player.buffer = "Only alphanumeric characters are permitted.\n"
    elif argument == PrintArg.NAME_NOT_WITHIN_PARAMS:
        player.buffer = "Provide an alphanumeric NAME that is at least " + OutgoingDefs.NAMES_MIN.value
        player.buffer += " characters long, and no more than " + printLineMax
        player.buffer += " characters. Try again.\n\nWhat is your NAME.\n"
    elif argument == PrintArg.PRINT_PROVIDE_NEW_ROOM_NAME:
        player.buffer = "Enter a new room name, of up to " + printLineMax + " chars.\n"
    elif argument == PrintArg.PRINT_PROVIDE_NEW_ROOM_DESC:
        player.buffer = "Enter a new room description, of up to " + bufLenMax + " chars.\n"
    elif argument == PrintArg.PRINT_CONFIRM_NEW_ROOM_DESC:
        player.buffer = "Confirm the new description by typing Y/y. You entered:\n" + player.store
        player.buffer += "\nIf this is wrong, type something other than Y/y.\n\n"
    elif argument == PrintArg.PRINT_CONFIRM_NEW_ROOM_NAME:
        player.buffer = "Confirm the new name by typing Y/y. You entered:\n" + player.store
        player.buffer += "\nIf this is wrong, type something other than Y/y.\n\n"
    elif argument == PrintArg.PRINT_ADJUSTMENT_SUCCESSFUL:
        player.buffer = "Room adjusted successfully. Exiting editor.\n"
    elif argument == PrintArg.PRINT_COULDNT_ADJUST_ROOM:
        player.buffer = "An error occurred. Room adjustment failed. Exiting editor.\n"
    elif argument == PrintArg.PRINT_EXITING_CMD_WAIT:
        player.buffer = "Exiting editor - returning you to the (real) world.\n"
    elif argument == PrintArg.PRINT_INSUFFICIENT_PERMISSIONS:
        player.buffer = "You don't have permission to do that.\n"
    elif argument == PrintArg.PRINT_ROOM_EXIT_CHANGED:
        player.buffer = "Room exit changed.\n"
    elif argument == PrintArg.PRINT_ROOM_FLAG_CHANGED:
        player.buffer = "Room flag toggled.\n"
    elif argument == PrintArg.PRINT_ROOM_REMOVAL_CHECK:
        player.buffer = "You're trying to delete this room. Are you sure you want to do this?\nType only y/Y to confirm.\n\n"
    elif argument == PrintArg.PRINT_ROOM_REMOVAL_CONFIRM:
        player.buffer = "Again, confirm that you want to delete your CURRENT ROOM.\n"
    elif argument == PrintArg.PRINT_ROOM_REMOVAL_SUCCESS:
        player.buffer = "Room removed successfully.\n"
    elif argument == PrintArg.PRINT_ROOM_REMOVAL_FAILURE:
        player.buffer = "Room removal failed - you are not the owner of this room.\n"
    elif argument == PrintArg.PRINT_ROOM_CREATION_GIVE_DIR:
        player.buffer = "Which direction are you trying to create a room in? (from current)\n"
    elif argument == PrintArg.PRINT_ROOM_CREATION_CONFIRMALL:
        player.buffer = "You're adding a room in the direction of: " + player.store
        player.buffer += ". Confirm this by typing y/Y, or decline by typing anything else.\n"
    elif argument == PrintArg.PRINT_ROOM_CREATION_CANNOT:
        player.buffer = "Room creation couldn't be completed right now.\n"
    elif argument == PrintArg.PRINT_ROOM_CREATION_SUCCESS:
        player.buffer = "Room creation complete.\n"
    elif argument == PrintArg.PRINT_ROOM_ALREADY_EXISTS:
        player.buffer = "A room already exists in that direction. Exiting editor.\n"
    elif argument == PrintArg.PRINT_ROOM_CREATION_FAILURE:
        player.buffer = "Creation failed. Contact an administrator.\n"
    elif argument == PrintArg.PRINT_REMOVED_FROM_ROOM:
        player.buffer = "You've been moved from your previous room the owner may have deleted it.\nMoved to:\n\n"
    elif argument == PrintArg.PRINT_PROVIDE_ROOM_EXIT_NAME:
        player.buffer = "Which direction are you trying to toggle exit visibility for?\n"
    elif argument == PrintArg.PRINT_PROVIDE_ROOM_FLAG_NAME:
        player.buffer = "Which flag are you trying to toggle?\n"
    elif argument == PrintArg.PRINT_TOGGLED_ROOM_EXIT:
        player.buffer = "Room exit visibility toggled. Exiting editor.\n"
    elif argument == PrintArg.PRINT_COULDNT_TOGGLE_EXIT:
        player.buffer = "Unable to toggle the exit for that room.\n"
    elif argument == PrintArg.PRINT_COULDNT_EXIT_NO_ROOM:
        player.buffer = "There's no room in that direction.\n"
    else:
        if 0 <= argument <= 19:
            set_buffer_for_movement(player, argument)

    if OutgoingHandler.send_and_handle_errors(player, len(player.buffer)) == 0:
        return 0
    else:
        command = CommandClasses.Command()
        command.type = CommandClasses.SystemAction
        command.subtype = CommandClasses.SystemAction.SYS_QUIT
        CommandExecutor.do_cmd_action(player, command)
        return 1


def set_buffer_for_movement(player, argument):
    # use enums
    base = "You move "
    if argument == 0:
        base += "NORTH.\n"
    elif argument == 2:
        base += "EAST.\n"
    elif argument == 4:
        base += "SOUTH.\n"
    elif argument == 6:
        base += "WEST.\n"
    elif argument == 8:
        base += "UP.\n"
    elif argument == 10:
        base += "DOWN.\n"
    elif argument == 12:
        base += "NORTHEAST.\n"
    elif argument == 14:
        base += "SOUTHEAST.\n"
    elif argument == 16:
        base += "SOUTHWEST.\n"
    elif argument == 18:
        base += "NORTHWEST.\n"
    else:
        return 1

    player.buffer = base

    return 0


def is_in_same_room(player, room_coords):
    playerCoords = player.coordinates
    return playerCoords.x == room_coords.x and playerCoords.y == room_coords.y and playerCoords.z == room_coords.z


def print_room_to_player(player, room):
    player.buffer = "NULL SPACE" if not room.found else room.rname

    append_coordinates_for_printing(player, room.coords)
    assert OutgoingHandler.send_and_handle_errors(player) == 0

    player.buffer = "Exits:"

    if SpaceClasses.RoomExits.NORTH_EXIT in room.exits:
        player.buffer += " N"
    if SpaceClasses.RoomExits.SOUTH_EXIT in room.exits:
        player.buffer += " S"
    if SpaceClasses.RoomExits.EAST_EXIT in room.exits:
        player.buffer += " E"
    if SpaceClasses.RoomExits.WEST_EXIT in room.exits:
        player.buffer += " W"
    if SpaceClasses.RoomExits.UP_EXIT in room.exits:
        player.buffer += " U"
    if SpaceClasses.RoomExits.DOWN_EXIT in room.exits:
        player.buffer += " D"
    if SpaceClasses.RoomExits.NORTHEAST_EXIT in room.exits:
        player.buffer += " NE"
    if SpaceClasses.RoomExits.SOUTHEAST_EXIT in room.exits:
        player.buffer += " SE"
    if SpaceClasses.RoomExits.SOUTHWEST_EXIT in room.exits:
        player.buffer += " SW"
    if SpaceClasses.RoomExits.NORTHWEST_EXIT in room.exits:
        player.buffer += " NW"

    if len(player.buffer) == 6:
        player.buffer += " NONE"

    assert OutgoingHandler.send_and_handle_errors(player) == 0

    player.buffer = "It is pitch black. You are likely to be eaten by a grue." if room.found == False else room.rdesc

    if room.rdesc and len(room.rdesc) > 0:
        player.buffer += "\n"

    assert OutgoingHandler.send_and_handle_errors(player) == 0

    for i in len(PlayerManagementLive.ActivePlayers):
        each = PlayerManagementLive.ActivePlayers[i]

        if each.name == player.name:
            continue

        if is_in_same_room(each, room.coords):
            player.buffer = each.name + " is here too.\n"
            # can be compressed instead of per loop
            assert OutgoingHandler.send_and_handle_errors(player) == 0

    return 0


def append_coordinates_for_printing(player, coords):
    player.buffer += " [" + coords.x + "][" + coords.y + "][" + coords.z + "]"


def print_all_commands(player):
    commands_on_line = 0
    player.buffer = "Available commands:\n"

    for i in CommandClasses.get_total_available_commands():
        cmd = CommandClasses.get_command_from_total_list(i)

        if len(player.buffer) + len(cmd) > 1024:
            assert OutgoingHandler.send_and_handle_errors(player) == 0

        if len(player.buffer) == 0:
            player.buffer = cmd
        else:
            player.buffer += cmd

        if ++commands_on_line < 5:
            player.buffer += "\t"
            if len(cmd) < 7:
                player.buffer += "\t"

        if commands_on_line == 5:
            commands_on_line = 0
            assert OutgoingHandler.send_and_handle_errors(player) == 0

    if len(player.buffer) != 0:
        player.buffer += "\n"

    assert OutgoingHandler.send_and_handle_errors(player) == 0

    return 0


def greet_player(socket):
    player = PlayerManagementLive.get_player(socket)
    player.buffer = "WELCOME.\n\n"
    player.buffer += "Please provide a NAME this can be two words and up to " + NAMES_MAX_STR
    player.buffer += " characters long in total.\n\nIf you've already created a character, enter your previous name to resume.\n\n"

    assert OutgoingHandler.send_and_handle_errors(player) == 0
    return 0


def print_player_speech(player):
    # check string lengths etc when working
    SKIP_SAY_TOKEN = 4
    playerSpeech = player.name + " says: "
    baseSay = player.buffer[SKIP_SAY_TOKEN:]
    playerSpeech += baseSay

    print_to_other_players(player, playerSpeech)

    print("print_player_speech to others " + playerSpeech)
    player.buffer = "You say: " + baseSay
    print("print_player_speech to them: " + player.buffer + " len " + len(
        player.buffer))

    assert OutgoingHandler.send_and_handle_errors(player) == 0
    return 0


def print_to_other_players(player, buffer):
    for i in len(PlayerManagementLive.ActivePlayers):
        otherPlayer = PlayerManagementLive[i]
        print("show it to player " + otherPlayer.name)

        if otherPlayer.socket_num == player.socket_num:
            continue

        if is_in_same_room(otherPlayer, player.coords):
            otherPlayer.buffer = buffer + "\n"
            assert OutgoingHandler.send_and_handle_errors(otherPlayer) == 0

    return 0
