from src.io import OutputBuilder
from src.io.CommandInterpreter import RoomChange, get_command_info
from src.io.OutputBuilder import print_to_player, print_room_to_player
from src.io.PrintArg import PrintArg
#from src.players.PlayerMovement import calc_coords_from_playerloc_and_dir
from src.players.PlayerWaitStates import PlayerWaitStates
import src.players.PlayerMovement
import src.players.PlayerManagement
from src.rooms.RoomClasses import RoomBlueprint
from ..sqlitehelper import SQLiteHelper
from . import RoomClasses


def adjust_room_name(player):
    if compare_room_owner(player, player.coords) == -1:
        return 2

    return SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET name = :store, last_modified_by = %Q WHERE x = %Q AND y = %Q AND z = %Q",
        {"name": player.store, "last_modified_by": player.name,
         "x": player.coords.x, "y": player.coords.y, "z": player.coords.z},
        SQLiteHelper.DBTypes.ROOM_DB)


def adjust_room_desc(player):
    if compare_room_owner(player, player.coords) == -1:
        return 2

    return SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET desc = :store, last_modified_by = %Q WHERE x = %Q AND y = %Q AND z = %Q",
        {"name": player.store, "last_modified_by": player.name,
         "x": player.coords.x, "y": player.coords.y, "z": player.coords.z},
        SQLiteHelper.DBTypes.ROOM_DB)


def adjust_room_flag(player):
    if compare_room_owner(player, player.coords) == -1:
        return 2

    return SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET flags = :store, last_modified_by = %Q WHERE x = %Q AND y = %Q AND z = %Q",
        {"name": player.store, "last_modified_by": player.name,
         "x": player.coords.x, "y": player.coords.y, "z": player.coords.z},
        SQLiteHelper.DBTypes.ROOM_DB)


def link_rooms(dir, existing, newroom):
    result = SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET :dir = :rid WHERE x = :x AND y = :y AND z = :z",
        {"dir": get_dir_str(dir), "rid": existing.r_id,
         "x": existing.x, "y": existing.y, "z": existing.z},
        SQLiteHelper.DBTypes.ROOM_DB)

    if result.results() is None:
        return 1

    result = SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET :dir = :rid WHERE x = :x AND y = :y AND z = :z",
        {"dir": get_dir_str_opposite(dir), "rid": newroom.r_id,
         "x": newroom.x, "y": newroom.y, "z": newroom.z},
        SQLiteHelper.DBTypes.ROOM_DB)

    if result.results() is None:
        return 1


def unlink_rooms(direction, existing, newroom):
    result = SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET %Q = '-1' WHERE x = :x AND y = :y AND z = :z",
        {"exit": get_dir_str(direction), "x": existing.x, "y": existing.y,
         "z": existing.z},
        SQLiteHelper.DBTypes.ROOM_DB)

    if result.results() is None:
        return 1

    result = SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET %Q = '-1' WHERE x = :x AND y = :y AND z = :z",
        {"exit": get_dir_str_opposite(direction), "x": newroom.x,
         "y": newroom.y, "z": newroom.z},
        SQLiteHelper.DBTypes.ROOM_DB)

    if result.results() is None:
        return 1

    return 0


def insert_room(rconfig):
    result = SQLiteHelper.SQLExecution(
        "INSERT INTO ROOMS (name, desc, x, y, z, north, east, south, west, up, down, "
        "northeast, southeast, southwest, northwest, owner, last_modified_by, flags) "
        "VALUES (:name, :desc, :x, :y, :z, :north, :east, :south, :west, "
        ":up, :down, :northeast, :southeast, :southwest, :northwest, :owner, :last_modified_by, :flags)",
        {"name": rconfig.name, "desc": rconfig.desc, "x": rconfig.x,
         "y": rconfig.y, "z": rconfig.z,
         "north": "-1", "east": "-1", "south": "-1", "west": "-1", "up": "-1",
         "down": "-1",
         "northeast": "-1", "southeast": "-1", "southwest": "-1",
         "northwest": "-1",
         "owner": rconfig.owner, "last_modified_by": rconfig.owner,
         "flags": rconfig.flags},
        SQLiteHelper.DBTypes.ROOM_DB)

    if result.results() is None:
        return None

    return lookup_room(rconfig.coords)


def remove_room(player):
    roomResult = lookup_room(player.coords)
    if roomResult is None:
        return -1

    if roomResult.results().owner is not player.name:
        return -2

    check_exits_and_adjust(player.coords, roomResult.results())

    queryResult = SQLiteHelper.SQLExecution(
        "DELETE FROM ROOMS WHERE x = :x AND y = :y AND z = :z",
        {"x": player.coords.x, "y": player.coords.y, "z": player.coords.z},
        SQLiteHelper.DBTypes.ROOM_DB)

    if queryResult.results is None:
        return 1

    return 0


def check_exits_and_adjust(coords, room):
    evacuate_to = 0

    for i in range(0, 10):
        if room.exits[i] == -1:
            continue

        roomResult = lookup_room_by_id(room.exits[i])

        if roomResult.results is None:
            continue

        if evacuate_to == 0:
            evacuate_to = roomResult.rid

        print("finding linked room: id " + str(roomResult.rid))
        actual = exit_to_dir(i)
        print("removing link " + str(actual) + " " + get_dir_str(actual))
        unlink_rooms(actual, room, roomResult.results())

    assert remove_players_from_room(coords, room) == 0


def exit_to_dir(room_exit):
    if room_exit == RoomClasses.RoomExits.NORTH_EXIT:
        return RoomClasses.RoomExits.DIR_NORTH
    if room_exit == RoomClasses.RoomExits.EAST_EXIT:
        return RoomClasses.RoomExits.DIR_EAST
    if room_exit == RoomClasses.RoomExits.SOUTH_EXIT:
        return RoomClasses.RoomExits.DIR_SOUTH
    if room_exit == RoomClasses.RoomExits.WEST_EXIT:
        return RoomClasses.RoomExits.DIR_WEST
    if room_exit == RoomClasses.RoomExits.UP_EXIT:
        return RoomClasses.RoomExits.DIR_UP
    if room_exit == RoomClasses.RoomExits.DOWN_EXIT:
        return RoomClasses.RoomExits.DIR_DOWN
    if room_exit == RoomClasses.RoomExits.NORTHEAST_EXIT:
        return RoomClasses.RoomExits.DIR_NORTHEAST
    if room_exit == RoomClasses.RoomExits.SOUTHEAST_EXIT:
        return RoomClasses.RoomExits.DIR_SOUTHEAST
    if room_exit == RoomClasses.RoomExits.SOUTHWEST_EXIT:
        return RoomClasses.RoomExits.DIR_SOUTHWEST
    if room_exit == RoomClasses.RoomExits.NORTHWEST_EXIT:
        return RoomClasses.RoomExits.DIR_NORTHWEST
    return -1


def remove_players_from_room(coords, target_room, players_in_room):
    from src.io.OutputBuilder import print_to_player, print_room_to_player
    from src.players.PlayerManagement import get_player_by_id, adjust_player_location
    queryResult = players_in_room(target_room.rid)

    for i in range(0, len(queryResult.results)):
        if queryResult.results[i].id == 0:
            break

        player = get_player_by_id(queryResult.results[i].id)

        if not player.coords.x == coords.x and player.coords.y == coords.y and player.coords.z == coords.z:
            continue

        print_to_player(player, OutputBuilder.PrintArg.PRINT_REMOVED_FROM_ROOM)
        room = lookup_room(coords)
        adjust_player_location(player, room.rid)
        room = lookup_room(player.coords)
        print_room_to_player(player, room)

    return 0


def lookup_room(coords):
    queryResult = SQLiteHelper.SQLExecution(
        "SELECT * FROM ROOMS WHERE x = :x AND y = :y AND z = :z",
        {"x": coords.x, "y": coords.y, "z": coords.z},
        SQLiteHelper.DBTypes.ROOM_DB)

    if queryResult.results is None:
        return None

    return queryResult


def lookup_room_by_id(r_id):
    queryResult = SQLiteHelper.SQLExecution(
        "SELECT * FROM ROOMS WHERE id = :id",
        {"id": r_id}, SQLiteHelper.DBTypes.ROOM_DB)

    if queryResult.results is None:
        return None

    return queryResult


def lookup_room_exits(origin, dest_room):
    origin_room = lookup_room(origin)
    if origin_room is None:
        return -2

    if has_exit_for_dir(origin_room.results(), dest_room) is 1:
        return -1

    return 0


def has_exit_for_dir(origin, dest):
    for i in range(0, 10):
        if dest.exits[i] == -1:
            continue
        if origin.id is dest.exits[i]:
            return 0

    return 1


def lookup_room_name_from_coords(player, coords):
    roomResult = lookup_room(coords)

    if roomResult is not None:
        player.buffer = roomResult.results().name
    else:
        player.buffer = "NULL SPACE"

    return 0


def compare_room_owner(player, coords):
    roomResult = lookup_room(coords)

    if player.name is roomResult.results().owner:
        return 1

    return 0


def get_dir_str_opposite(direction):
    dirToString = {
        RoomClasses.Direction.NORTH: "south",
        RoomClasses.Direction.EAST: "west",
        RoomClasses.Direction.SOUTH: "north",
        RoomClasses.Direction.WEST: "east",
        RoomClasses.Direction.UP: "down",
        RoomClasses.Direction.DOWN: "up",
        RoomClasses.Direction.NORTHEAST: "southwest",
        RoomClasses.Direction.SOUTHEAST: "northwest",
        RoomClasses.Direction.SOUTHWEST: "northeast",
        RoomClasses.Direction.NORTHWEST: "southeast",
    }
    if direction in list(dirToString.values()):
        return list(dirToString.values())[direction]

    return "nowhere"


def get_dir_str(direction):
    dirToString = {
        RoomClasses.Direction.NORTH: "north",
        RoomClasses.Direction.EAST: "east",
        RoomClasses.Direction.SOUTH: "south",
        RoomClasses.Direction.WEST: "west",
        RoomClasses.Direction.UP: "up",
        RoomClasses.Direction.DOWN: "down",
        RoomClasses.Direction.NORTHEAST: "northeast",
        RoomClasses.Direction.SOUTHEAST: "southeast",
        RoomClasses.Direction.SOUTHWEST: "southwest",
        RoomClasses.Direction.NORTHWEST: "northwest",
    }
    if direction in list(dirToString.values()):
        print("movement string is " + list(dirToString.values())[direction])
        return list(dirToString.values())[direction]

    return "nowhere"


def alter_room_links(player, command):
    if (src.players.PlayerManagement.ensure_player_moving_valid_dir(player, command)) == 1:
        src.players.PlayerManagement.reset_player_state(player)
        return 1

    dest_coords = src.players.PlayerMovement.calc_coords_from_playerloc_and_dir(player)
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

    reset(player)


def alter_room_desc(player, command):
    if command is not None and command[0] is not 'y':
        print_to_player(player, PrintArg.PRINT_EXITING_CMD_WAIT)
        src.players.PlayerManagement.reset_player_state(player)

    result = adjust_room_desc(player)
    if result == 0:
        print_to_player(player, PrintArg.PRINT_ADJUSTMENT_SUCCESSFUL)
    elif result is 1:
        print_to_player(player, PrintArg.PRINT_COULDNT_ADJUST_ROOM)
    elif result is 2:
        print_to_player(player, PrintArg.PRINT_INSUFFICIENT_PERMISSIONS)

    reset(player)
    roomResult = lookup_room(player.coords)
    print_room_to_player(player, roomResult)


def alter_room_name(player, command):
    if command is not None and command[0] is not 'y':
        print_to_player(player, PrintArg.PRINT_EXITING_CMD_WAIT)
        reset()

    result = adjust_room_name(player)
    if result == 0:
        print_to_player(player, PrintArg.PRINT_ADJUSTMENT_SUCCESSFUL)
    elif result == 1:
        print_to_player(player, PrintArg.PRINT_COULDNT_ADJUST_ROOM)
    elif result == 2:
        print_to_player(player, PrintArg.PRINT_INSUFFICIENT_PERMISSIONS)

    reset(player)
    roomResult = lookup_room(player.coords)
    print_room_to_player(player, roomResult)


def handle_room_creation(player, command):
    if command is not None and command[0] is not 'y':
        print_to_player(player, PrintArg.PRINT_EXITING_CMD_WAIT)
        reset(player)

    dest_coords = src.players.PlayerMovement.calc_coords_from_playerloc_and_dir(player)
    roomResult = lookup_room(dest_coords)

    if roomResult.id > 0:
        print_to_player(player, PrintArg.PRINT_ROOM_ALREADY_EXISTS)
        reset(player)
        return

    # check here for their perms
    # print_to_player(player, PRINT_INSUFFICIENT_PERMISSIONS)

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
    reset(player)


def handle_room_removal(player, command):
    if command is not None and command[0] is not 'y':
        print_to_player(player, PrintArg.PRINT_EXITING_CMD_WAIT)
        reset(player)

    # TODO: check exits etc handled & players in room moved
    result = remove_room(player)
    if result == 0:
        print_to_player(player, PrintArg.PRINT_ROOM_REMOVAL_SUCCESS)
    elif result == -1:
        print_to_player(player, PrintArg.PRINT_ROOM_REMOVAL_FAILURE)
    elif result == -2:
        print_to_player(player, PrintArg.PRINT_INSUFFICIENT_PERMISSIONS)

    reset(player)


def prepare_for_new_room_desc(player, command):
    player.store = command
    player.wait_state = PlayerWaitStates.WAIT_CONFIRM_NEW_ROOM_DESC
    print_to_player(player, PrintArg.PRINT_CONFIRM_NEW_ROOM_DESC)


def prepare_for_new_room_name(player, command):
    player.store = command
    player.wait_state = PlayerWaitStates.WAIT_CONFIRM_NEW_ROOM_NAME
    print_to_player(player, PrintArg.PRINT_CONFIRM_NEW_ROOM_NAME)


def prepare_for_room_mk(player, command):
    if src.players.PlayerManagement.ensure_player_moving_valid_dir(player, command) is 1:
        reset(player)
        return

    player.store = command
    player.wait_state = PlayerWaitStates.WAIT_ROOM_CREATION_CONF
    print_to_player(player, PrintArg.PRINT_ROOM_CREATION_CONFIRMALL)


def prepare_for_room_rm(player):
    print_to_player(player, PrintArg.PRINT_ROOM_REMOVAL_CONFIRM)
    player.wait_state = PlayerWaitStates.WAIT_ROOM_REMOVAL_CONFIRM


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


def reset(player):
    src.players.PlayerManagement.reset_player_state(player)
