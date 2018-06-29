from enum import Enum, auto

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
	#define IS_DIRECTION_ARG (argument >= 0 && argument <= 19)

	if argument == PrintArg.PRINT_INVAL_CMD:
		player.buffer = "Invalid command. Type \'commands\'.\n"
	elif argument == PrintArg.SHOW_CMDS:
		print_all_commands(player)
	elif argument == PrintArg.PRINT_INVAL_DIR:
		player.buffer = "Cannot move in that direction. Type 'look' to view room.\n"
	elif argument == PrintArg.REQUEST_PW_FOR_NEW:
		player.buffer = "You've provided the name ["
		player.buffer += player.name
		player.buffer += "].\n\n"
		player.buffer += "Provide a password less than "
		player.buffer += BUFFER_LENGTH_STR
		player.buffer += " characters long.\n\n"
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
		player.buffer = "Provide an alphanumeric NAME that is at least "
		player.buffer += NAMES_MIN_STR
		player.buffer += " characters long, and no more than "
		player.buffer += NAMES_MAX_STR
		player.buffer += " characters. Try again.\n\nWhat is your NAME.\n"
	elif argument == PrintArg.PRINT_PROVIDE_NEW_ROOM_NAME:
		player.buffer = "Enter a new room name, of up to "
		player.buffer += MAX_ROOM_NAME_STR
		player.buffer += " chars.\n"
	elif argument == PrintArg.PRINT_PROVIDE_NEW_ROOM_DESC:
		player.buffer = "Enter a new room description, of up to "
		player.buffer += BUFFER_LENGTH_STR
		player.buffer += " chars.\n"
	elif argument == PrintArg.PRINT_CONFIRM_NEW_ROOM_DESC:
		player.buffer = "Confirm the new description by typing Y/y. You entered:\n"
		player.buffer += player.store
		player.buffer += "\nIf this is wrong, type something other than Y/y.\n\n"
	elif argument == PrintArg.PRINT_CONFIRM_NEW_ROOM_NAME:
		player.buffer = "Confirm the new name by typing Y/y. You entered:\n"
		player.buffer += player.store
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
		player.buffer = "You're adding a room in the direction of: "
		player.buffer += player.store
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
		if IS_DIRECTION_ARG:
			set_buffer_for_movement(player, argument)

	assert(outgoing_handler(player) == 0)
	return 0


def set_buffer_for_movement (player, argument):
    if argument == 0:
		player.buffer = "You move NORTH.\n"
    elif argument == 2:
		player.buffer = "You move EAST.\n"
    elif argument == 4:
		player.buffer = "You move SOUTH.\n"
    elif argument == 6:
		player.buffer = "You move WEST.\n"
    elif argument == 8:
		player.buffer = "You move UP.\n"
    elif argument == 10:
		player.buffer = "You move DOWN.\n"
    elif argument == 12:
		player.buffer = "You move NORTHEAST.\n"
    elif argument == 14:
		player.buffer = "You move SOUTHEAST.\n"
    elif argument == 16:
		player.buffer = "You move SOUTHWEST.\n"
    elif argument == 18:
		player.buffer = "You move NORTHWEST.\n"
    else:
		return 1

    return 0


def is_in_same_room(player, room_coords):
	struct coordinates coords = get_player_coords(player)

	return coords.x == room_coords.x && coords.y == room_coords.y && 
		coords.z == room_coords.z

def print_room_to_player(player, room):
	player.buffer =
			(room.found == false) ? (void *)"NULL SPACE" : (void *)room.rname)

	append_coordinates_for_printing(player, room.coords)
	assert(outgoing_handler(player) == 0)

	player.buffer = "Exits:"

	if (room.exits[NORTH_EXIT] >= 0)
		player.buffer += " N"
	if (room.exits[SOUTH_EXIT] >= 0)
		player.buffer += " S"
	if (room.exits[EAST_EXIT] >= 0)
		player.buffer += " E"
	if (room.exits[WEST_EXIT] >= 0)
		player.buffer += " W"
	if (room.exits[UP_EXIT] >= 0)
		player.buffer += " U"
	if (room.exits[DOWN_EXIT] >= 0)
		player.buffer += " D"
	if (room.exits[NORTHEAST_EXIT] >= 0)
		player.buffer += " NE"
	if (room.exits[SOUTHEAST_EXIT] >= 0)
		player.buffer += " SE"
	if (room.exits[SOUTHWEST_EXIT] >= 0)
		player.buffer += " SW"
	if (room.exits[NORTHWEST_EXIT] >= 0)
		player.buffer += " NW"

	if (strlen((char *)player.buffer) == 6)
		player.buffer += " NONE"

	assert(outgoing_handler(player) == 0)

	player.buffer =
			(room .found == false) ?
			(void *)"It is pitch black. You are "
			"likely to be eaten by a null character."
			: (void *)room.rdesc)

	if (room.rdesc != NULL && strlen((char *)room.rdesc) > 0)
		player.buffer += "\n"
	assert(outgoing_handler(player) == 0)

	const uint8_t *target = player.name

	for (size_t i = 0 i < get_num_of_players(); ++i) {
		struct player_live_record *each = get_player_by_index(i)

		if (each.name == target)
			continue

		if (is_in_same_room(each, room.coords) == true) {
			player.buffer = each.name)
			player.buffer += " is here too.\n"
			assert(outgoing_handler(player) == 0)
		}
	}

	return 0

def append_coordinates_for_printing(player, coords):
	uint8_t param_x[sizeof(coords.x)] = {0}
	uint8_t param_y[sizeof(coords.y)] = {0}
	uint8_t param_z[sizeof(coords.z)] = {0}
	snprintf((char *)param_x, sizeof(coords.x), "%d", coords.x)
	snprintf((char *)param_y, sizeof(coords.y), "%d", coords.y)
	snprintf((char *)param_z, sizeof(coords.z), "%d", coords.z)

	player.buffer += " ["
	player.buffer += param_x)
	player.buffer += "]["
	player.buffer += param_y)
	player.buffer += "]["
	player.buffer += param_z)
	player.buffer += "]"

def print_all_commands(player):
	int32_t commands_on_line = 0
	size_t player_buffer_len
	void *cmd

	player.buffer = "Available commands:\n"

	for (size_t i = 0 i < get_num_of_available_cmds(); ++i) {
		cmd = get_command(i)
		player_buffer_len = strlen((char *)player.buffer)

		if (strlen((char *)player.buffer) + strlen((char *)cmd) > BUFFER_LENGTH) {
			assert(outgoing_handler(player) == 0)
			player_buffer_len = 0
		}

		if (player_buffer_len == 0) {
			player.buffer = cmd)
		} else {
			player.buffer += cmd)
		}

		if (++commands_on_line < 5) {
			player.buffer += "\t"
			if (strlen((char *)cmd) < 7)
				player.buffer += "\t"
		}

		if (commands_on_line == 5) {
			commands_on_line = 0
			assert(outgoing_handler(player) == 0)
		}
	}

	if (strlen((char *)player.buffer) != 0)
		player.buffer += "\n"

	assert(outgoing_handler(player) == 0)

	return true

def greet_player(socket):
	struct player_live_record *player = get_player(socket)
	player.buffer = "WELCOME.\n\n"
	player.buffer += "Please provide a NAME this can be two words and up to ";
	player.buffer += NAMES_MAX_STR
	player.buffer += " characters long in total.\n\nIf you've "
			"already created a character, enter your previous name to resume.\n\n"

	assert(outgoing_handler(player) == 0)
	return 0

def print_player_speech(player):
	#define SKIP_SAY_TOKEN 4 // length req'd for the actual say command + the space after that
	uint8_t *buffer = calloc(BUFFER_LENGTH+1, sizeof(uint8_t))
	void *loc_in_buf = NULL

	loc_in_buf = mempcpy(buffer, player.name, strlen((char *)player.name))
	loc_in_buf = mempcpy(loc_in_buf, " says: ", 7)

	int32_t to_add = strlen((char *)&player.buffer[SKIP_SAY_TOKEN])
	if (to_add + strlen((char *)buffer) > BUFFER_LENGTH)
		to_add = BUFFER_LENGTH - strlen((char *)buffer)

	loc_in_buf = mempcpy(loc_in_buf, &player.buffer[SKIP_SAY_TOKEN], to_add)

	print_to_other_players(player, buffer)

#ifdef DEBUG
	print("print_player_speech to others: %s\n", buffer)
#endif

	free(buffer)

	uint8_t substr[to_add]
	memset(substr, '\0', to_add)

	memcpy(substr, "You say: ", 9)
	memcpy(&substr[9], &player.buffer[SKIP_SAY_TOKEN], to_add)
	memcpy(&substr[9+to_add], "\n", 1)

	player.buffer = substr)

#ifdef DEBUG
	print("print_player_speech to them: %s (%lu)\n", player.buffer, strlen((char *)player.buffer))
#endif

	assert(outgoing_handler(player) == 0)

	return 0

def print_to_other_players(player, buffer):
	struct coordinates coords = get_player_coords(player)

	for (size_t i = 0 i < get_num_of_players(); ++i) {
		struct player_live_record *present = get_player_by_index(i)

		printf("show it to player %s?\n", present.name)

		if (present.socket_num == player.socket_num)
			continue

		if (is_in_same_room(present, coords) == true) {
			set_player_buffer_replace(present, buffer)
			set_player_buffer_append(present, "\n"
			assert(outgoing_handler(present) == 0)
		}
	}

	return 0