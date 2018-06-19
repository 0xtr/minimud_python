def calc_coords_from_playerloc_and_dir(player):
	Coords coords = get_player_coords(player)

	if not player.store:
		coords.x = coords.y = coords.z = -1
		return coords

	# WHAT
	struct command *info = (struct command *)calloc(sizeof(struct command), 
			sizeof(struct command))

	info->type = COMMAND_NOT
	info->subtype = COMMAND_NOT

	info = is_movement_cmd(player->store, info)

	coords.x += x_movement_to_vector(info)
	coords.y += y_movement_to_vector(info)
	coords.z += z_movement_to_vector(info)

	return coords

def x_movement_to_vector(info):
	if any(info.subtype in i for i in (DIR_EAST, DIR_NORTHEAST, DIR_SOUTHEAST)):
		return 1
	elif any(info.subtype in i for i in (DIR_SOUTHWEST, DIR_NORTHWEST, DIR_WEST)):
		return -1

	return 0

def y_movement_to_vector(info):
	if any(info.subtype in i for i in (DIR_NORTH, DIR_NORTHEAST, DIR_NORTHWEST)):
		return 1
	elif any(info.subtype in i for i in (DIR_SOUTHEAST, DIR_SOUTHWEST, DIR_SOUTH)):
		return -1

	return 0

def z_movement_to_vector(info):
	if (info.subtype == DIR_UP):
		return 1
	elif (info.subtype == DIR_DOWN):
		return -1

	return 0