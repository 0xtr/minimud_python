class RoomDBRecord:
	id = ''
	found = False
	rname = ''
	rdesc = ''
	owner = ''
	lastModifiedBy = ''
	Coords = []
	exits = []


class Coords:
	x, y, z = 0;


class RoomBlueprint:
	name = ''
	desc = ''
	owner = ''
	flags = []
	Coords = []
