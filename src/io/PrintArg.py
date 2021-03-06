from enum import Enum, auto


class PrintArg(Enum):
    PLAYER_INVALID_CMD = auto()
    PLAYER_INVALID_DIR = auto()
    PLAYER_REQUEST_PW_FOR_NEW = auto()
    PLAYER_SHOW_COMMANDS = auto()
    PLAYER_REQUEST_PW_CONFIRM = auto()
    PLAYER_REQUEST_PW_FOR_EXISTING = auto()
    PLAYER_ATTEMPT_CREATE_USR = auto()
    PLAYER_MISMATCH_PW_SET = auto()
    PLAYER_CREATION_FAILED = auto()
    PLAYER_CREATION_SUCCESS = auto()
    PLAYER_ALREADY_ONLINE = auto()
    PLAYER_INCORRECT_PASSWORD = auto()
    PLAYER_UNABLE_TO_RETRIEVE_CHAR = auto()
    PLAYER_NAME_UNAVAILABLE = auto()
    PLAYER_ALPHANUM_NAMES_ONLY = auto()
    PLAYER_NAME_NOT_WITHIN_PARAMS = auto()
    ROOM_PROVIDE_NEW_NAME = auto()
    ROOM_PROVIDE_NEW_DESC = auto()
    ROOM_CONFIRM_NEW_DESC = auto()
    ROOM_CONFIRM_NEW_NAME = auto()
    ROOM_ADJUSTMENT_SUCCESSFUL = auto()
    ROOM_COULDNT_ADJUST_ROOM = auto()
    ROOM_EXIT_CHANGED = auto()
    ROOM_FLAG_CHANGED = auto()
    ROOM_REMOVAL_CHECK = auto()
    ROOM_REMOVAL_CONFIRM = auto()
    ROOM_REMOVAL_SUCCESS = auto()
    ROOM_REMOVAL_FAILURE = auto()
    ROOM_CREATION_GIVE_DIR = auto()
    ROOM_CREATION_CONFIRMALL = auto()
    ROOM_CREATION_FAIL = auto()
    ROOM_CREATION_SUCCESS = auto()
    ROOM_ALREADY_EXISTS = auto()
    ROOM_CREATION_FAILURE = auto()
    ROOM_REMOVED_FROM_ROOM = auto()
    ROOM_PROVIDE_EXIT_NAME = auto()
    ROOM_PROVIDE_FLAG_NAME = auto()
    ROOM_TOGGLED_EXIT = auto()
    ROOM_COULDNT_TOGGLE_EXIT = auto()
    ROOM_COULDNT_EXIT_NO_ROOM = auto()
    EXITING_CMD_WAIT = auto()
    INSUFFICIENT_PERMISSIONS = auto()
