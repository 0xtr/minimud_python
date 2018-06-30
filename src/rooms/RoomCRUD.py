from ..sqlitehelper import SQLiteHelper

#define player_is_not_owner memcmp(map->owner, player->name, strlen((char *)map->owner))

def adjust_room_name(player):
    if compare_room_owner(player, player.coords) == -1:
        return 2

    return SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET name = :store, last_modified_by = %Q WHERE x = %Q AND y = %Q AND z = %Q",
        {"name":player.store,"last_modified_by":player.name,
         "x":player.coords.x,"y":player.coords.y,"z":player.coords.z},
        SQLiteHelper.DBTypes.ROOM_DB)

def adjust_room_desc(player):
    if (compare_room_owner(player, player.coords) == -1)
        return 2

    return SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET desc = :store, last_modified_by = %Q WHERE x = %Q AND y = %Q AND z = %Q",
        {"name":player.store,"last_modified_by":player.name,
         "x":player.coords.x,"y":player.coords.y,"z":player.coords.z},
        SQLiteHelper.DBTypes.ROOM_DB)

def adjust_room_flag(player):
    if (compare_room_owner(player, player.coords) == -1)
        return 2

    return SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET flags = :store, last_modified_by = %Q WHERE x = %Q AND y = %Q AND z = %Q",
        {"name":player.store,"last_modified_by":player.name,
         "x":player.coords.x,"y":player.coords.y,"z":player.coords.z},
        SQLiteHelper.DBTypes.ROOM_DB)

def link_rooms(dir, existing, newroom):
    result = SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET :dir = :rid WHERE x = :x AND y = :y AND z = :z",
        {"dir":get_movement_str(dir), "rid":existing.r_id,
         "x":existing.x,"y":existing.y,"z":existing.z},
        SQLiteHelper.DBTypes.ROOM_DB)

    if result.results is None:
        return 1

    result = SQLiteHelper.SQLExecution(
        "UPDATE ROOMS SET :dir = :rid WHERE x = :x AND y = :y AND z = :z",
        {"dir":get_opposite_string(dir), "rid":newroom.r_id,
         "x":newroom.x,"y":newroom.y,"z":newroom.z},
        SQLiteHelper.DBTypes.ROOM_DB)

    if result.results is None:
        return 1

def unlink_rooms(dir, existing, newroom)
    int32_t rv = run_sql(sqlite3_mprintf(
        "UPDATE ROOMS SET %Q = '-1' WHERE x = %Q AND y = %Q AND z = %Q",
        get_movement_str(dir), param_x, param_y, param_z), 0, DB_ROOM)

    if (rv == EXIT_FAILURE)
        return rv

    snprintf((char *)param_x, sizeof(newroom->coords.x), "%d", newroom->coords.x)
    snprintf((char *)param_y, sizeof(newroom->coords.y), "%d", newroom->coords.y)
    snprintf((char *)param_z, sizeof(newroom->coords.z), "%d", newroom->coords.z)

    return run_sql(sqlite3_mprintf(
        "UPDATE ROOMS SET %Q = '-1' WHERE x = %Q AND y = %Q AND z = %Q",
        get_opposite_str(dir), param_x, param_y, param_z), 0, DB_ROOM)

def insert_room(rconfig)
    uint8_t param_x[2 * sizeof(rconfig.coords.x)] = {0}
    uint8_t param_y[2 * sizeof(rconfig.coords.y)] = {0}
    uint8_t param_z[2 * sizeof(rconfig.coords.z)] = {0}
    snprintf((char *)param_x, sizeof(rconfig.coords.x), "%d", rconfig.coords.x)
    snprintf((char *)param_y, sizeof(rconfig.coords.y), "%d", rconfig.coords.y)
    snprintf((char *)param_z, sizeof(rconfig.coords.z), "%d", rconfig.coords.z)

    run_sql(sqlite3_mprintf(
        "INSERT INTO ROOMS (name, desc, x, y, z, north, east, south, west, up, down, "
        "northeast, southeast, southwest, northwest, owner, last_modified_by, flags) "
        "VALUES (%Q, %Q, %Q, %Q, %Q, %Q, %Q, %Q, %Q, %Q, %Q, %Q, %Q, %Q, %Q, %Q, %Q, %Q)",
        (char *)rconfig.name, (char *)rconfig.desc,
        param_x, param_y, param_z,
        "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1",
        (char *)rconfig.owner, (char *)rconfig.owner, (char *)rconfig.flags), 0, DB_ROOM)

    struct room_db_record *room = lookup_room(rconfig.coords)

    return room

def remove_room(player):
    struct coordinates coords = get_player_coords(player)
    struct room_db_record *map = lookup_room(coords)

    if (map == NULL)
        return -1

    if (player_is_not_owner) {
        free(map)
        return -2
    }

    //convert_coords_into_string_params(coords.x, coords.y, coords.z)
    convert_coords_into_string_params(coords)

    check_exits_and_adjust(coords, map)

    int32_t rv = run_sql(sqlite3_mprintf(
            "DELETE FROM ROOMS WHERE x = %Q AND y = %Q AND z = %Q",
            param_x, param_y, param_z), 0, DB_ROOM)
    if (rv == EXIT_FAILURE) {
        free(map)
        return EXIT_FAILURE
    }

    free(map)

    return EXIT_SUCCESS

def check_exits_and_adjust(coords, room):
    int32_t evacuate_to = 0

    for (size_t i = 0 i < 10; ++i) {
        if (room->exits[i] == -1)
            continue

        struct room_db_record *target = lookup_room_by_id(room->exits[i])

        if (target == NULL)
            continue

        if (evacuate_to == 0)
            evacuate_to = target->id

        printf("finding linked room: id %d\n", target->id)

        int32_t actual = exit_to_dir(i)
        printf("removing link %d %s\n", actual, get_movement_str(actual))

        unlink_rooms(actual, room, target)

        free(target)
    }

    assert(remove_players_from_room(coords, room) == EXIT_SUCCESS)

def exit_to_dir(const int32_t exit):
    if (exit == NORTH_EXIT)
        return DIR_NORTH
    if (exit == EAST_EXIT)
        return DIR_EAST
    if (exit == SOUTH_EXIT)
        return DIR_SOUTH
    if (exit == WEST_EXIT)
        return DIR_WEST
    if (exit == UP_EXIT)
        return DIR_UP
    if (exit == DOWN_EXIT)
        return DIR_DOWN
    if (exit == NORTHEAST_EXIT)
        return DIR_NORTHEAST
    if (exit == SOUTHEAST_EXIT)
        return DIR_SOUTHEAST
    if (exit == SOUTHWEST_EXIT)
        return DIR_SOUTHWEST
    if (exit == NORTHWEST_EXIT)
        return DIR_NORTHWEST
    return -1

def remove_players_from_room(coords, room):
    struct query_matches *qmatches = players_in_room(room->id)

    for (size_t i = 0 i < qmatches->matches; ++i) {
        if (qmatches->ids[i] == 0)
            break

        struct player_live_record *player = get_player_by_id(qmatches->ids[i])
        struct coordinates this = get_player_coords(player)

        if (!(this.x == coords.x && this.y == coords.y
                    && this.z == coords.z))
            continue

        print_to_player(player, PRINT_REMOVED_FROM_ROOM)

        struct room_db_record *room = lookup_room(coords)

        adjust_player_location(player, room->id)
        // check results

        free(room) // get the updated room image
        room = lookup_room(get_player_coords(player))

        print_room_to_player(player, room)

        free(room)
    }

    free(qmatches)

    return EXIT_SUCCESS

def lookup_room(coords)
    convert_coords_into_string_params(coords)

    struct room_db_record *map = get_room()

    int32_t rv = run_sql(sqlite3_mprintf(
            "SELECT * FROM ROOMS WHERE x = %Q AND y = %Q AND z = %Q",
            param_x, param_y, param_z), map, DB_ROOM)

    if (rv == EXIT_FAILURE)
        return NULL

    return map

def lookup_room_by_id(id):
    uint8_t idstr[2 * sizeof(id)] = {0}
    snprintf((char *)idstr, sizeof(id), "%d", id)

    struct room_db_record *map = get_room()

    int32_t rv = run_sql(sqlite3_mprintf(
            "SELECT * FROM ROOMS WHERE id = %Q", idstr), map, DB_ROOM);

    if (rv == EXIT_FAILURE)
        return NULL

    return map

def lookup_room_exits(origin, dest_room):
    int32_t rv = 0
    struct room_db_record *origin_room = lookup_room(origin)

    if (dest_room == NULL) {
        rv = -2
        goto end
    }

    if (has_exit_for_dir(origin_room, dest_room) == EXIT_FAILURE)
        rv = -1

    end:

    free(origin_room)

    return rv

def has_exit_for_dir(origin, dest):
    for (size_t i = 0 i < 10; ++i) {
        if (dest->exits[i] == -1)
            continue

        if (memcmp(&origin->id, &dest->exits[i], sizeof(int32_t)) == 0)
            return EXIT_SUCCESS
    }

    return EXIT_FAILURE

def lookup_room_name_from_coords(player, coords):
    struct room_db_record *map = lookup_room(coords)

    if (map != NULL) {
        // get_room_details(map)
        set_player_buffer_replace(player, map->rname)
        free(map)
    } else {
        set_player_buffer_replace(player, "NULL SPACE")
    }

    return EXIT_SUCCESS

def compare_room_owner(player, coords):
    int32_t rv = EXIT_SUCCESS
    struct room_db_record *map = lookup_room(coords)

    if (strcmp((char*)player->name, (char*)map->owner) != 0)
        rv = EXIT_FAILURE

    free(map)

    return rv