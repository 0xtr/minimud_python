from enum import Enum, auto
from src.rooms import SpaceClasses


class Movement(Enum):
    DIR_NORTH = auto()
    DIR_N = auto()
    DIR_EAST = auto()
    DIR_E = auto()
    DIR_SOUTH = auto()
    DIR_S = auto()
    DIR_WEST = auto()
    DIR_W = auto()
    DIR_UP = auto()
    DIR_U = auto()
    DIR_DOWN = auto()
    DIR_D = auto()
    DIR_NORTHEAST = auto()
    DIR_NE = auto()
    DIR_SOUTHEAST = auto()
    DIR_SE = auto()
    DIR_SOUTHWEST = auto()
    DIR_SW = auto()
    DIR_NORTHWEST = auto()
    DIR_NW = auto()
    DIR_NOT = auto()


class CommandTypes(Enum):
    MOVEMENT = auto()
    ROOM_CHANGE = auto()
    SYSTEM_ACTION = auto()
    TRAVEL_ACTION = auto()
    INFO_REQUEST = auto()
    COMMAND_NOT = -1


class SystemAction(Enum):
    SYS_SAY = auto()
    SYS_QUIT = auto()
    SYS_NOT = auto()


class RoomChange(Enum):
    ROOM_ADD = auto()
    ROOM_REMOVE = auto()
    ROOM_SET_NAME = auto()
    ROOM_SET_DESC = auto()
    ROOM_SET_FLAG = auto()
    ROOM_SET_EXIT = auto()
    ROOM_SET_NOT = auto()


class InfoRequest(Enum):
    INFO_ROOM = auto()
    INFO_ROOM2 = auto()
    INFO_PLAYERS = auto()
    INFO_MAP = auto()
    INFO_COMMANDS = auto()
    INFO_COMMANDS2 = auto()
    INFO_COMMANDS3 = auto()
    INFO_NOT = auto()


class TravelAction(Enum):
    TRAVEL_GOTO = auto()
    TRAVEL_SWAP = auto()
    TRAVEL_NOT = auto()


class Command:
    type = CommandTypes.COMMAND_NOT
    subtype = CommandTypes.COMMAND_NOT
    commandList = {
        CommandTypes.MOVEMENT, ["north", "n", "east", "e", "south", "s", "west", "w",
                                "up", "u", "down", "d", "northeast", "ne", "southeast",
                                "se", "southwest", "sw", "northwest", "nw"],
        CommandTypes.SYSTEM_ACTION, ["say", "quit"],
        CommandTypes.INFO_REQUEST, ["look", "l", "players", "map", "commands", "?", "help"],
        CommandTypes.ROOM_CHANGE, ["mkroom", "rmroom", "setrname", "setrdesc", "setrexit", "setrflag"],
        CommandTypes.TRAVEL_ACTION, ["goto", "swap"]
    }


def get_available_commands(void):
    num = 0
    for i in Command.commandList.keys():
        num += Command.commandList[i].len
    print("command num is " + num)
    return num


def is_actual_direction(dir, check):
    return dir == check or dir == (check + 1)


def categorize_command(num):
    command = Command()
    # magic
    return command
