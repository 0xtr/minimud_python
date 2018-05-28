struct room_db_record {
	int32_t id;

	_Bool found;

	uint8_t rname[NAMES_MAX];
	uint8_t rdesc[BUFFER_LENGTH];
	uint8_t owner[NAMES_MAX];
	uint8_t last_modified[NAMES_MAX];

	struct coordinates coords;

	int32_t exits[10];
}; 

struct coordinates {
	int32_t x;
	int32_t y;
	int32_t z;
};

struct room_blueprint {
	uint8_t *name;
	uint8_t *desc;

	struct coordinates coords;

	uint8_t *owner;
	uint8_t *flags;
};

def get_room():
	return (struct room_db_record *)calloc(sizeof(struct room_db_record), sizeof(struct room_db_record));