from enum import Enum, auto


class RoomDBRecord:
    id = ''
    found = False
    rname = ''
    rdesc = ''
    owner = ''
    lastModifiedBy = ''
    Coords = []
    exits = []


class RoomBlueprint:
    name = ''
    desc = ''
    owner = ''
    flags = []
    Coords = []


class Coordinates:
    x, y, z = [-1, -1, -1]


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()
    UP = auto()
    DOWN = auto()
    NORTHEAST = auto()
    SOUTHEAST = auto()
    SOUTHWEST = auto()
    NORTHWEST = auto()


class RoomExits(Enum):
    NORTH_EXIT = auto()
    EAST_EXIT = auto()
    SOUTH_EXIT = auto()
    WEST_EXIT = auto()
    UP_EXIT = auto()
    DOWN_EXIT = auto()
    NORTHEAST_EXIT = auto()
    SOUTHEAST_EXIT = auto()
    SOUTHWEST_EXIT = auto()
    NORTHWEST_EXIT = auto()

