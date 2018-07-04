# define not_waiting_for_player_response \
from src.io import OutputBuilder
from src.io.IncomingHandler import check_if_name_is_valid, \
    check_if_name_is_reserved, check_if_player_is_already_online
from src.io.OutputBuilder import print_to_player, PrintArg, print_room_to_player
from src.players.PlayerCRUD import ensure_player_moving_valid_dir, lookup_player
from src.players.PlayerManagementLive import reset_player_state
from src.players.PlayerMovement import calc_coords_from_playerloc_and_dir
from src.rooms.RoomCRUD import adjust_room_desc, lookup_room, adjust_room_name, \
    insert_room, link_rooms, remove_room
from src.rooms.SpaceClasses import RoomBlueprint


def interpret_command(player):
    command = process_buffer(player)
    commandInfo = get_command_info(command)

    if (not_waiting_for_player_response)
        if (info->type == COMMAND_NOT) {
        print_to_player(player, INVALCMD)
        free(info)

        return EXIT_FAILURE

        return do_cmd_action(player, info)

    # should probably handle 'quit' if they want to exit this process, or C - C
    switch(player.wait_state):
        case THEIR_NAME: \
                handle_incoming_name(player, command)
                break
                case
                THEIR_PASSWORD_EXISTING:
                handle_existing_pass(player, command)
                break


case
THEIR_PASSWORD_NEWPRELIM:
set_player_confirm_new_pw(player, command)
break
case
THEIR_PASSWORD_NEWFINAL:
handle_new_pass(player, command)
break

case
WAIT_ENTER_NEW_ROOM_NAME:
prepare_for_new_room_name(player, command)
break
case
WAIT_CONFIRM_NEW_ROOM_NAME:
alter_room_name(player, command)
break

case
WAIT_ENTER_NEW_ROOM_DESC:
prepare_for_new_room_desc(player, command)
break
case
WAIT_CONFIRM_NEW_ROOM_DESC:
alter_room_desc(player, command)
break

case
WAIT_ROOM_REMOVAL_CHECK:
prepare_for_room_rm(player)
break
case
WAIT_ROOM_REMOVAL_CONFIRM:
handle_room_removal(player, command)
break

case
WAIT_ROOM_CREATION_DIR:
prepare_for_room_mk(player, command)
break
case
WAIT_ROOM_CREATION_CONF:
handle_room_creation(player, command)
break

// TODO
case
WAIT_ENTER_FLAG_NAME:
// CHECK_IF_IS_VALID_FLAG
// finish
reset_player_state(player)
break
// TODO
case
WAIT_ENTER_EXIT_NAME:
alter_room_links(player, command)
break
default:
fprintf(stdout, "Unhandled wait state %d on player %s.\n",
        player->wait_state, player->name)
}

free(command)
free(info)
return EXIT_SUCCESS


def alter_room_links(player, command):
    if ((ensure_player_moving_valid_dir(player, command)) == EXIT_FAILURE) {
    reset_player_state(player)
    return
    }

    int32_t
    rv
    struct
    coordinates
    player_coords = get_player_coords(player)
    struct
    coordinates
    dest_coords = calc_coords_from_playerloc_and_dir(player)
    struct
    room_db_record * src_room = lookup_room(player_coords)
    struct
    room_db_record * dest_room = lookup_room(dest_coords)

    if (dest_room == NULL) {
    print_to_player(player, PRINT_COULDNT_EXIT_NO_ROOM)
    goto
    failed

}

if (compare_room_owner(player, player_coords) == EXIT_FAILURE) {
print_to_player(player, PRINT_INSUFFICIENT_PERMISSIONS)
goto
failed
}

struct command * info = get_command_info(command) const
int32_t dir = info->subtype

rv = link_rooms(dir, src_room, dest_room)

if (rv == EXIT_SUCCESS)
{
print_to_player(player, PRINT_TOGGLED_ROOM_EXIT)
} else if (rv == EXIT_FAILURE) {
print_to_player(player, PRINT_COULDNT_TOGGLE_EXIT)
}

failed:

if (src_room != NULL)
free(src_room)
if (dest_room != NULL)
free(dest_room)

reset_player_state(player)
}


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
        print_to_player(player, PRINT_ROOM_ALREADY_EXISTS)
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
        return;

    print_to_player(player, PRINT_ROOM_CREATION_SUCCESS)

    struct command * info = get_command_info(player->store)
    const int32_t dir = info->subtype free(info)

    link_rooms(dir, existing, new)

    existing = lookup_room(player.coords
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
    elif rv == -1:
        print_to_player(player, PrintArg.PRINT_ROOM_REMOVAL_FAILURE)
    elif rv == -2:
        print_to_player(player, PrintArg.PRINT_INSUFFICIENT_PERMISSIONS)

    reset_player_state(player)


def process_buffer(player):
    size_t len = strlen((char *) player->buffer)

    if (player->wait_state == THEIR_NAME)
        len = NAMES_MAX

    uint8_t * command = calloc(len + 1, sizeof(uint8_t))

    for (size_t i = 0 i < len; ++i) {
        command[i] = player->buffer[i]
    if (command[i] == '\0')
    break

    if (player->wait_state != THEIR_NAME) {
    if (isupper(command[i]) != 0)
    command[i] = tolower(command[i])

    if (isspace(command[i]) != 0) {
    command[i] = '\0'
    break


return command


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
        player.wait_state = THEIR_PASSWORD_EXISTING
    else:
        print_to_player(player, PrintArg.REQUEST_PW_FOR_NEW)
        player.wait_state = THEIR_PASSWORD_NEWPRELIM

    return True

// TODO: use
enums


def prepare_for_new_room_desc(player, command):
    player.store = command
    player.wait_state = WAIT_CONFIRM_NEW_ROOM_DESC
    print_to_player(player, PrintArg.PRINT_CONFIRM_NEW_ROOM_DESC)


def prepare_for_new_room_name(player, command):
    player.store = command
    player.wait_state = WAIT_CONFIRM_NEW_ROOM_NAME
    print_to_player(player, PrintArg.PRINT_CONFIRM_NEW_ROOM_NAME)


def prepare_for_room_mk(player, command):
    if (ensure_player_moving_valid_dir(player, command)) is 1:
        reset_player_state(player)
        return

    player.store = command
    player.wait_state = WAIT_ROOM_CREATION_CONF

    print_to_player(player, PrintArg.PRINT_ROOM_CREATION_CONFIRMALL)


def prepare_for_room_rm(player):
    OutputBuilder.print_to_player(player, PrintArg.PRINT_ROOM_REMOVAL_CONFIRM)
    player.wait_state = WAIT_ROOM_REMOVAL_CONFIRM
