from enum import Enum, auto


def get_command_info(command):
    newCommand = Command()
    commandList = Command.getCompleteList()
    for commandType in list(commandList):
        commands = commandList[commandType]
        if command in commands.values():
            newCommand.type = commandType
            newCommand.subtype = commands[command]
            break

    print("newCommand: " + str(newCommand.type))
    return newCommand


def get_available_commands():
    num = 0
    commands = Command.getCompleteList()
    for i in commands.keys():
        num += len(commands[i])
    print("command num is " + num)
    return num


class Movement(Enum):
    DIR_NORTH = auto()
    DIR_EAST = auto()
    DIR_SOUTH = auto()
    DIR_WEST = auto()
    DIR_UP = auto()
    DIR_DOWN = auto()
    DIR_NORTHEAST = auto()
    DIR_SOUTHEAST = auto()
    DIR_SOUTHWEST = auto()
    DIR_NORTHWEST = auto()
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
    INFO_PLAYERS = auto()
    INFO_MAP = auto()
    INFO_COMMANDS = auto()
    INFO_NOT = auto()


class TravelAction(Enum):
    TRAVEL_GOTO = auto()
    TRAVEL_SWAP = auto()
    TRAVEL_NOT = auto()


class Command:
    type = CommandTypes.COMMAND_NOT
    subtype = CommandTypes.COMMAND_NOT

    @staticmethod
    def getCompleteList():
        return {
            CommandTypes.MOVEMENT:
                {"north": Movement.DIR_NORTH, "n": Movement.DIR_NORTH,
                 "east": Movement.DIR_EAST, "e": Movement.DIR_EAST,
                 "south": Movement.DIR_SOUTH, "s": Movement.DIR_SOUTH,
                 "west": Movement.DIR_WEST, "w": Movement.DIR_WEST,
                 "up": Movement.DIR_UP, "u": Movement.DIR_UP,
                 "down": Movement.DIR_DOWN, "d": Movement.DIR_DOWN,
                 "northeast": Movement.DIR_NORTHEAST,
                 "ne": Movement.DIR_NORTHEAST,
                 "southeast": Movement.DIR_SOUTHEAST,
                 "se": Movement.DIR_SOUTHEAST,
                 "southwest": Movement.DIR_SOUTHWEST,
                 "sw": Movement.DIR_SOUTHWEST,
                 "northwest": Movement.DIR_NORTHWEST,
                 "nw": Movement.DIR_NORTHWEST},
            CommandTypes.SYSTEM_ACTION:
                {"say": SystemAction.SYS_SAY,
                 "quit": SystemAction.SYS_QUIT},
            CommandTypes.INFO_REQUEST:
                {"look": InfoRequest.INFO_ROOM, "l": InfoRequest.INFO_ROOM,
                 "players": InfoRequest.INFO_PLAYERS,
                 "map": InfoRequest.INFO_MAP,
                 "commands": InfoRequest.INFO_COMMANDS,
                 "?": InfoRequest.INFO_COMMANDS,
                 "help": InfoRequest.INFO_COMMANDS},
            CommandTypes.ROOM_CHANGE:
                {"mkroom": RoomChange.ROOM_ADD,
                 "rmroom": RoomChange.ROOM_REMOVE,
                 "setrname": RoomChange.ROOM_SET_NAME,
                 "setrdesc": RoomChange.ROOM_SET_DESC,
                 "setrexit": RoomChange.ROOM_SET_EXIT,
                 "setrflag": RoomChange.ROOM_SET_FLAG},
            CommandTypes.TRAVEL_ACTION:
                {"goto": TravelAction.TRAVEL_GOTO,
                 "swap": TravelAction.TRAVEL_SWAP}
        }


def get_all_commands_as_strings():
    stringList = []
    commandList = Command.getCompleteList()
    for commandType in list(commandList):
        stringList.append(list(commandList[commandType]))

    print("commands: " + str(stringList))
    return stringList


def is_actual_direction(direction, check):
    return direction == check or direction == (check + 1)
