def get_player_coords(player):
	struct player_db_record *player_db = get_player_db_struct();
	struct coordinates coords;
	coords.x = coords.y = coords.z = -1;

	run_sql(sqlite3_mprintf("SELECT * FROM PLAYERS WHERE name = %Q;", player->name), player_db, DB_PLAYER);

	struct room_db_record *room = lookup_room_by_id(player_db->loc_id);
	coords = room->coords;

	free(player_db);
	free(room);

	return coords;

def get_player_loc_id(player):
	struct player_db_record *player_db = get_player_db_struct();

	run_sql(sqlite3_mprintf("SELECT * FROM PLAYERS WHERE name = %Q;", player->name), player_db, DB_PLAYER);

	const int32_t loc_id = player_db->loc_id;

	free(player_db);

	return loc_id;

def get_next_player_num():
	struct query_matches *qmatches = init_query();

	assert(run_sql("SELECT id FROM PLAYERS;", qmatches, 
				DB_PLAYER_COUNT) == EXIT_SUCCESS);
	const int32_t max_id = qmatches->matches;

	free(qmatches);

	return max_id;