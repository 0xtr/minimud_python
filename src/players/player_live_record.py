struct player_live_record {
	int32_t db_id;

	_Bool   connected;
	_Bool   holding_for_input;
	int32_t wait_state;
	int32_t socket_num;

	uint8_t name[NAMES_MAX];
	uint8_t buffer[BUFFER_LENGTH];
	void *loc_in_buf;

	struct  sockaddr *restrict address;
	socklen_t address_len;

	uint8_t *store;
	void *loc_in_store;
	int32_t store_size;

	struct player_live_record *prev;
	struct player_live_record *next;
	struct Inventory *inventory;
};

def get_player(socket):
	struct player_live_record *curr = head;

	if (curr != NULL) {
		while (curr != NULL) {
			if (curr->socket_num == socket)
				break;
			curr = curr->next;
		}
	}

	return curr;

def get_player_by_id(id):
	struct player_live_record *curr = head;

	if (curr != NULL) {
		while (curr != NULL) {
			if (curr->db_id == id)
				break;
			curr = curr->next;
		}
	}

	return curr;

def get_player_head(void):
	return head;

def get_player_by_index(index):
	struct player_live_record *curr = head;

	if (curr == NULL)
		return NULL;

	for (size_t i = 0; i < index; ++i) {
		if (curr == NULL)
			return NULL;

		curr = curr->next;
	}

	return curr;

def remove_last_player_record():
	if (tail == NULL)
		return EXIT_FAILURE;

	struct player_live_record *curr = tail;

	curr = tail->prev;
	free(tail);

	curr->next = NULL;
	tail = curr;

	return EXIT_SUCCESS;

def remove_player_by_socket(socket):
	struct player_live_record *curr = get_player(socket);

	struct player_live_record *prev = curr->prev;
	struct player_live_record *next = curr->next;

	if (tail == curr)
		tail = curr->prev;
	if (head == curr)
		head = curr->next;

	printf("remove by socket %d\n", socket);
	free(curr);

	if (prev != NULL)
		prev->next = next;
	if (next != NULL)
		next->prev = prev;

	return EXIT_SUCCESS;

def int32_t add_new_player(socket):
	struct player_live_record *curr = (struct player_live_record *)calloc(
			sizeof(struct player_live_record), sizeof(struct player_live_record));

	if (curr == NULL)
		return EXIT_FAILURE;

	curr->db_id = -1;
    	curr->socket_num = socket;
    	curr->inventory = get_new_player_inventory(socket);
	curr->holding_for_input = true;
	curr->wait_state = THEIR_NAME;
	curr->prev = tail;

	if (tail != NULL)
		tail->next = curr;

	tail = curr;

	if (head == NULL)
		head = curr;

	return EXIT_SUCCESS;

def set_player_name(player, name):
	memcpy(player->name, name, strlen((char *)name));

	return EXIT_SUCCESS;

def set_player_store_replace(player, newval):
	memset(player->store, '\0', player->store_size);

	int32_t len = strlen((char *)newval);
	if (len > BUFFER_LENGTH)
		len = BUFFER_LENGTH;

	memcpy(player->store, newval, len);
	player->store_size = len;

	return EXIT_SUCCESS;

def set_player_store_append(player, new):
	if (strlen((char *)player->store) + strlen((char *)new) > BUFFER_LENGTH)
		return EXIT_FAILURE;

	memcpy(&player->store[strlen((char *)player->store)], new, strlen((char *)new));

	return EXIT_SUCCESS;

def clear_player_buffer(player):
	memset(player->buffer, 0, BUFFER_LENGTH);
	player->loc_in_buf = NULL;

	return EXIT_SUCCESS;

def init_player_store(player):
	if (player->store != NULL)
		free(player->store);

	player->store = calloc(BUFFER_LENGTH+1, sizeof(uint8_t));
	player->store_size = strlen((char *)player->buffer);
	memcpy(player->store, player->buffer, strlen((char *)player->buffer));

	return EXIT_SUCCESS;

def clear_player_store(player):
	if (player->store_size == 0)
		return EXIT_SUCCESS;

	memset(player->store, '\0', player->store_size);
	free(player->store);
	player->store = NULL;
	player->store_size = 0;

	return EXIT_SUCCESS;

def set_player_buffer_replace(player, newbuf):
	int32_t len = strlen((char *)newbuf);
	if (len > BUFFER_LENGTH)
		len = BUFFER_LENGTH;

	player->loc_in_buf = mempcpy(player->buffer, newbuf, len);

	return EXIT_SUCCESS;

def set_player_buffer_append(player, append):
	if (strlen((char *)player->buffer) + strlen((char *)append) > BUFFER_LENGTH)
		return EXIT_FAILURE;

	player->loc_in_buf = mempcpy(player->loc_in_buf, append, strlen((char *)append));

	return EXIT_SUCCESS;

def get_num_of_players():
	size_t list_size = 0;
	struct player_live_record *tmp = head;

	if (tmp == NULL)
		return list_size;

	if (tmp->connected == true)
		++list_size;

	while (tmp->next != NULL) {
		if (tmp->connected == true)
			++list_size;

		tmp = tmp->next;
	}

	return list_size;

def reset_player_state(player):
	player.wait_state = NO_WAIT_STATE;
	player.holding_for_input = 0;
	clear_player_store(player);
	return player;

def store_player_id(player, id):
	player.db_id = id;
	return player;

def get_player_id(socket):
	return get_player(socket).db_id;

def get_socket_by_id(const int32_t id):
	return get_player_by_id(id).socket_num;