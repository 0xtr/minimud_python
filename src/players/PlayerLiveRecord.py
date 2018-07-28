from src.items.Inventory import Inventory
import src.players.PlayerManagement


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

    def __init__(self, sock):
        self.connected = True
        self.db_id = -1
        self.socket = sock
        self.holding_for_input = True
        self.wait_state = src.players.PlayerManagement.PlayerWaitStates.THEIR_NAME


