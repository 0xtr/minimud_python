from src.io.CommandInterpreter import Command, Movement, TravelAction, \
    CommandTypes
from src.io.OutputBuilder import print_to_player, PrintArg, print_room_to_player
from src.rooms.RoomCRUD import lookup_room, lookup_room_exits
from src.rooms.RoomClasses import Direction, Coordinates
from src.sqlitehelper import SQLiteHelper


def calc_coords_from_playerloc_and_dir(player):
    if player.store is None:
        player.coords.x = player.coords.y = player.coords.z = -1
        return

    info = Command()
    info.type = CommandTypes.COMMAND_NOT
    info.subtype = CommandTypes.COMMAND_NOT

    coords = Coordinates()
    coords.x += x_movement_to_vector(info)
    coords.y += y_movement_to_vector(info)
    coords.z += z_movement_to_vector(info)

    return coords


def x_movement_to_vector(info):
    if any(info.subtype in i for i in (Direction.DIR_EAST,
                                       Direction.DIR_NORTHEAST,
                                       Direction.DIR_SOUTHEAST)):
        return 1
    elif any(info.subtype in i for i in (Direction.DIR_SOUTHWEST,
                                         Direction.DIR_NORTHWEST,
                                         Direction.DIR_WEST)):
        return -1

    return 0


def y_movement_to_vector(info):
    if any(info.subtype in i for i in (Direction.DIR_NORTH,
                                       Direction.DIR_NORTHEAST,
                                       Direction.DIR_NORTHWEST)):
        return 1
    elif any(info.subtype in i for i in (Direction.DIR_SOUTHEAST,
                                         Direction.DIR_SOUTHWEST,
                                         Direction.DIR_SOUTH)):
        return -1

    return 0


def z_movement_to_vector(info):
    if info.subtype == Direction.DIR_UP:
        return 1
    elif info.subtype == Direction.DIR_DOWN:
        return -1

    return 0


def do_movement_cmd(player, info):
    direction = Movement.DIR_NOT
    origin = player.coords
    destination = {0}

    if info.subtype == Movement.DIR_NORTH:
        direction = Movement.DIR_NORTH
        destination.y = origin.y + 1
    elif info.subtype == Movement.DIR_EAST:
        direction = Movement.DIR_EAST
        destination.x = origin.x + 1
    elif info.subtype == Movement.DIR_SOUTH:
        direction = Movement.DIR_SOUTH
        destination.y = origin.y - 1
    elif info.subtype == Movement.DIR_WEST:
        direction = Movement.DIR_WEST
        destination.x = origin.x - 1
    elif info.subtype == Movement.DIR_DOWN:
        direction = Movement.DIR_DOWN
        destination.z = origin.z - 1
    elif info.subtype == Movement.DIR_UP:
        direction = Movement.DIR_UP
        destination.z = origin.z + 1
    elif info.subtype == Movement.DIR_NORTHWEST:
        direction = Movement.DIR_NORTHWEST
        destination.x = origin.x - 1
        destination.y = origin.y + 1
    elif info.subtype == Movement.DIR_NORTHEAST:
        direction = Movement.DIR_NORTHEAST
        destination.x = origin.x + 1
        destination.y = origin.y + 1
    elif info.subtype == Movement.DIR_SOUTHWEST:
        direction = Movement.DIR_SOUTHWEST
        destination.x = origin.x - 1
        destination.y = origin.y - 1
    elif info.subtype == Movement.DIR_SOUTHEAST:
        direction = Movement.DIR_SOUTHEAST
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
        destination.x = 0
        destination.y = 0
        destination.z = 0
        print_to_player(player, PrintArg.PRINT_INVAL_DIR)
        # check me
    else:
        print_to_player(player, direction)

    adjust_player_location(player, dest_room.id)
    print_room_to_player(player, dest_room)


def do_travel_cmd(player, info):
    if info.subtype == TravelAction.TRAVEL_GOTO:
        print("ADD ME %d\n", player.socket_num)

    if info.subtype == TravelAction.TRAVEL_SWAP:
        print("ADD ME %d\n", player.socket_num)


def adjust_player_location(player, room_id):
    return SQLiteHelper.SQLExecution(
        "UPDATE PLAYERS SET loc_id =:room_id WHERE name =:pname",
        {"loc_id": room_id, "name": player.name},
        SQLiteHelper.DBTypes.PLAYER_DB)


