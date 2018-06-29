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

