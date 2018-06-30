from src.items import Inventory
from enum import Enum, auto


class PlayerWaitStates(Enum):
    THEIR_NAME = auto()
    THEIR_PASSWORD = auto()
    NO_WAIT_STATE = -1


class ActivePlayers:
    activePlayers = []


class PlayerLiveRecord:
    db_id = 0

    connected = False
    holding_for_input = False
    wait_state = 0
    socket = 0

    name = ''
    buffer = ''
    store = ''
    inventory = Inventory()


def get_player(socket):
    for player in ActivePlayers.activePlayers:
        if player.socket == socket:
            return player

    return None


def get_player_by_id(pid):
    for player in ActivePlayers.activePlayers:
        if player.db_id == pid:
            return player

    return None


def remove_player_by_socket(socket):
    print("remove by socket ", socket)
    ActivePlayers.activePlayers.remove(get_player(socket))
    # remove from select socklist?


def add_new_player(socket):
    player = PlayerLiveRecord()
    player.db_id = -1
    player.socket = socket
    player.holding_for_input = True
    player.wait_state = PlayerWaitStates.THEIR_NAME
    ActivePlayers.activePlayers.append(player)


def get_num_of_players():
    return len(ActivePlayers.activePlayers)


def reset_player_state(player):
    player.wait_state = PlayerWaitStates.NO_WAIT_STATE
    player.holding_for_input = False
    player.store = ''
