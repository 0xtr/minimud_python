from src.io import OutputBuilder
from src.io.OutputBuilder import print_to_player, print_room_to_player
from src.players.PlayerCRUD import players_in_room, adjust_player_location
from src.players.PlayerManagementLive import get_player_by_id
from ..sqlitehelper import SQLiteHelper
from . import SpaceClasses


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

    if result.results is None:
        return 1

    result = SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET :dir = :rid WHERE x = :x AND y = :y AND z = :z",
        {"dir": get_dir_str_opposite(dir), "rid": newroom.r_id,
         "x": newroom.x, "y": newroom.y, "z": newroom.z},
        SQLiteHelper.DBTypes.ROOM_DB)

    if result.results is None:
        return 1


def unlink_rooms(direction, existing, newroom):
    result = SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET %Q = '-1' WHERE x = :x AND y = :y AND z = :z",
        {"exit": get_dir_str(direction), "x": existing.x, "y": existing.y,
         "z": existing.z},
        SQLiteHelper.DBTypes.ROOM_DB)

    if result.results is None:
        return 1

    result = SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET %Q = '-1' WHERE x = :x AND y = :y AND z = :z",
        {"exit": get_dir_str_opposite(direction), "x": newroom.x,
         "y": newroom.y, "z": newroom.z},
        SQLiteHelper.DBTypes.ROOM_DB)

    if result.results is None:
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

    if result.results is None:
        return None

    return lookup_room(rconfig.coords)


def remove_room(player):
    roomResult = lookup_room(player.coords);
    if roomResult is None:
        return -1

    if roomResult.owner is not player.name:
        return -2

    check_exits_and_adjust(player.coords, roomResult)

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
        unlink_rooms(actual, room, roomResult)

    assert remove_players_from_room(coords, room) == 0


def exit_to_dir(room_exit):
    if room_exit == SpaceClasses.RoomExits.NORTH_EXIT:
        return SpaceClasses.RoomExits.DIR_NORTH
    if room_exit == SpaceClasses.RoomExits.EAST_EXIT:
        return SpaceClasses.RoomExits.DIR_EAST
    if room_exit == SpaceClasses.RoomExits.SOUTH_EXIT:
        return SpaceClasses.RoomExits.DIR_SOUTH
    if room_exit == SpaceClasses.RoomExits.WEST_EXIT:
        return SpaceClasses.RoomExits.DIR_WEST
    if room_exit == SpaceClasses.RoomExits.UP_EXIT:
        return SpaceClasses.RoomExits.DIR_UP
    if room_exit == SpaceClasses.RoomExits.DOWN_EXIT:
        return SpaceClasses.RoomExits.DIR_DOWN
    if room_exit == SpaceClasses.RoomExits.NORTHEAST_EXIT:
        return SpaceClasses.RoomExits.DIR_NORTHEAST
    if room_exit == SpaceClasses.RoomExits.SOUTHEAST_EXIT:
        return SpaceClasses.RoomExits.DIR_SOUTHEAST
    if room_exit == SpaceClasses.RoomExits.SOUTHWEST_EXIT:
        return SpaceClasses.RoomExits.DIR_SOUTHWEST
    if room_exit == SpaceClasses.RoomExits.NORTHWEST_EXIT:
        return SpaceClasses.RoomExits.DIR_NORTHWEST
    return -1


def remove_players_from_room(coords, target_room):
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

    if has_exit_for_dir(origin_room, dest_room) is 1:
        rv = -1

    return rv


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
        player.buffer = roomResult.name
    else:
        player.buffer = "NULL SPACE"

    return 0


def compare_room_owner(player, coords):
    roomResult = lookup_room(coords)

    if player.name is map.owner:
        return 1

    return 0


def get_dir_str_opposite(direction):
    dirToString = {
        SpaceClasses.Direction.NORTH, "south",
        SpaceClasses.Direction.EAST, "west",
        SpaceClasses.Direction.SOUTH, "north",
        SpaceClasses.Direction.WEST, "east",
        SpaceClasses.Direction.UP, "down",
        SpaceClasses.Direction.DOWN, "up",
        SpaceClasses.Direction.NORTHEAST, "southwest",
        SpaceClasses.Direction.SOUTHEAST, "northwest",
        SpaceClasses.Direction.SOUTHWEST, "northeast",
        SpaceClasses.Direction.NORTHWEST, "southeast",
    }
    if direction in dirToString:
        return dirToString[direction]

    return "nowhere"


def get_dir_str(direction):
    dirToString = {
        SpaceClasses.Direction.NORTH, "north",
        SpaceClasses.Direction.EAST, "east",
        SpaceClasses.Direction.SOUTH, "south",
        SpaceClasses.Direction.WEST, "west",
        SpaceClasses.Direction.UP, "up",
        SpaceClasses.Direction.DOWN, "down",
        SpaceClasses.Direction.NORTHEAST, "northeast",
        SpaceClasses.Direction.SOUTHEAST, "southeast",
        SpaceClasses.Direction.SOUTHWEST, "southwest",
        SpaceClasses.Direction.NORTHWEST, "northwest",
    }
    if direction in dirToString:
        print("movement string is " + dirToString[direction])
        return dirToString[direction]

    return "nowhere"
