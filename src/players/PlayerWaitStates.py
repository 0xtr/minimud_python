from enum import Enum, auto


class PlayerWaitStates(Enum):
    THEIR_NAME = auto()
    THEIR_PASSWORD_EXISTING = auto()
    THEIR_PASSWORD_NEWPRELIM = auto()
    THEIR_PASSWORD_NEWFINAL = auto()
    CONFIRM_THEIR_NEW_NAME = auto()
    NO_WAIT_STATE = -1


