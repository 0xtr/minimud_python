from ..sqlite_custom import SQLiteHelper
from ..spaces import SpaceClasses


class PlayerDBRecord:
    name = ''
    ourHash = ''
    salt = ''
    last_ip = ''
    id = -1
    loc_id = -1


def get_player_coords(player):
    player_db_record = PlayerDBRecord()
    SQLiteHelper.run_sql(
        sqlite3_mprintf("SELECT * FROM PLAYERS WHERE name = %Q;", player.name),
        player_db, DB_PLAYER)
    room_db_record = SpaceClasses.lookupRoomById(player_db_record.loc_id)
    return room_db_record.coordinates


# merge the two into just get_player_room
def get_player_loc_id(player):
    player_db_record = PlayerDBRecord()
    SQLiteHelper.run_sql(sqlite3_mprintf("SELECT * FROM PLAYERS WHERE name = %Q;", player->name), player_db, DB_PLAYER);
    return player_db_record.loc_id;


def insert_player(player, pw):
    uint8_t * salt = calloc(SALT_LENGTH + 1, sizeof(uint8_t));
    PASSWORD_LEN = (strlen((char *)pw) > BUFFER_LENGTH) ? BUFFER_LENGTH: strlen(
        (char *)
    pw);
    // reset_sqlite_rows_count();

    strcpy((char *) salt, bcrypt_gensalt(10)); // pretty weak

    uint8_t * salt_and_pw = calloc(BUFFER_LENGTH + SALT_LENGTH,
                                   sizeof(uint8_t));
    void * append_pw = mempcpy(salt_and_pw, salt, strlen((char *)
    salt));
    append_pw = mempcpy(append_pw, pw, PASSWORD_LEN);

    uint8_t * hash_result = calloc(HASH_LENGTH, sizeof(uint8_t));
    bcrypt_newhash((char *)
    salt_and_pw, 10, (char *)
    hash_result, HASH_LENGTH);

    int32_t
    rv = run_sql(sqlite3_mprintf(
        "INSERT INTO PLAYERS (name, hash, salt, last_ip, loc_id) "
        "VALUES (%Q, %Q, %Q, %Q, %Q);",
        (char *)
    player->name, (char *)
    hash_result, (char *)
    salt, "-", "0"), 0, DB_PLAYER);

    if (rv == EXIT_FAILURE)
        return EXIT_FAILURE;

    print_to_player(player, PLAYER_CREATION_SUCCESS);
    return EXIT_SUCCESS;


def lookup_player(name):
    player_db_record = PlayerDBRecord()
    SQLiteHelper.run_sql(sqlite3_mprintf("SELECT * FROM PLAYERS WHERE name = %Q;", name),
            player, DB_PLAYER);
    if player.id == -1:
        return None

    return player
