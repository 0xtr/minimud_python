from src.commands.CommandClasses import CommandTypes, SystemAction, InfoRequest, \
    RoomChange, Movement, TravelAction
from src.io.IncomingHandler import shutdown_socket
from src.io.OutputBuilder import print_player_speech, print_room_to_player, \
    print_to_player, PrintArg
from src.players.PlayerCRUD import adjust_player_location
from src.players.PlayerManagementLive import PlayerWaitStates
from src.rooms.RoomCRUD import lookup_room, lookup_room_exits


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


def do_info_cmd(player, info):
    if info.subtype == InfoRequest.INFO_ROOM or info.subtype == InfoRequest.INFO_ROOM2:
        roomResult = lookup_room(player.coords)
        print_room_to_player(player, roomResult.results())

    if info.subtype == InfoRequest.INFO_COMMANDS:
        print_to_player(player, PrintArg.SHOWCMDS)
    if info.subtype == InfoRequest.INFO_PLAYERS:
        print_to_player(player, PrintArg.LISTPLAYERS)
    if info.subtype == InfoRequest.INFO_MAP:
        print("ADD ME\n")


def do_room_cmd(player, info):
    if info.subtype == RoomChange.ROOM_SET_NAME:
        print_to_player(player, PrintArg.PRINT_PROVIDE_NEW_ROOM_NAME)
        player.holding_for_input = 1
        player.wait_state = PlayerWaitStates.WAIT_ENTER_NEW_ROOM_NAME
    elif info.subtype == RoomChange.ROOM_SET_DESC:
        print_to_player(player, PrintArg.PRINT_PROVIDE_NEW_ROOM_DESC)
        player.wait_state = PlayerWaitStates.WAIT_ENTER_NEW_ROOM_DESC
        player.holding_for_input = True
    elif info.subtype == RoomChange.ROOM_SET_EXIT:
        print_to_player(player, PrintArg.PRINT_PROVIDE_ROOM_EXIT_NAME)
        player.wait_state = PlayerWaitStates.WAIT_ENTER_EXIT_NAME
        player.holding_for_input = True
    elif info.subtype == RoomChange.ROOM_SET_FLAG:
        print_to_player(player, PrintArg.PRINT_PROVIDE_ROOM_FLAG_NAME)
        player.wait_state = PlayerWaitStates.WAIT_ENTER_FLAG_NAME
        player.holding_for_input = True
    elif info.subtype == RoomChange.ROOM_MK:
        print_to_player(player, PrintArg.PRINT_ROOM_CREATION_GIVE_DIR)
        player.wait_state = PlayerWaitStates.WAIT_ROOM_CREATION_DIR
        player.holding_for_input = True
    elif info.subtype == RoomChange.ROOM_RM:
        print_to_player(player, PrintArg.PRINT_ROOM_REMOVAL_CHECK)
        player.wait_state = PlayerWaitStates.WAIT_ROOM_REMOVAL_CHECK
        player.holding_for_input = True


def do_movement_cmd(player, info):
    dir = Movement.DIR_NOT
    origin = player.coords
    destination = {0}

    if info.subtype == Movement.DIR_NORTH:
        dir = Movement.DIR_NORTH
        destination.y = origin.y + 1
    elif info.subtype == Movement.DIR_EAST:
        dir = Movement.DIR_EAST
        destination.x = origin.x + 1
    elif info.subtype == Movement.DIR_SOUTH:
        dir = Movement.DIR_SOUTH
        destination.y = origin.y - 1
    elif info.subtype == Movement.DIR_WEST:
        dir = Movement.DIR_WEST
        destination.x = origin.x - 1
    elif info.subtype == Movement.DIR_DOWN:
        dir = Movement.DIR_DOWN
        destination.z = origin.z - 1
    elif info.subtype == Movement.DIR_UP:
        dir = Movement.DIR_UP
        destination.z = origin.z + 1
    elif info.subtype == Movement.DIR_NORTHWEST:
        dir = Movement.DIR_NORTHWEST
        destination.x = origin.x - 1
        destination.y = origin.y + 1
    elif info.subtype == Movement.DIR_NORTHEAST:
        dir = Movement.DIR_NORTHEAST
        destination.x = origin.x + 1
        destination.y = origin.y + 1
    elif info.subtype == Movement.DIR_SOUTHWEST:
        dir = Movement.DIR_SOUTHWEST
        destination.x = origin.x - 1
        destination.y = origin.y - 1
    elif info.subtype == Movement.DIR_SOUTHEAST:
        dir = Movement.DIR_SOUTHEAST
        destination.x = origin.x + 1
        destination.y = origin.y - 1

    dest_room = lookup_room(destination)
    if dest_room is None:
        print("oh no")
        # do something

    rv = lookup_room_exits(origin, dest_room)

    if rv == -1:
        print_to_player(player, PrintArg.PRINT_INVAL_DIR)
        return
    elif rv == -2:
        # send them back to origin room, somewhere they shouldn't be
        print_to_player(player, PrintArg.PRINT_INVAL_DIR)
        destination.x = 0
        destination.y = 0
        destination.z = 0
        # check this

    print_to_player(player, dir)
    adjust_player_location(player, dest_room.id)
    print_room_to_player(player, dest_room)


def do_travel_cmd(player, info):
    if info.subtype == TravelAction.TRAVEL_GOTO:
        print("ADD ME %d\n", player.socket_num)

    if info.subtype == TravelAction.TRAVEL_SWAP:
        print("ADD ME %d\n", player.socket_num)
