from src.items.Inventory import Inventory


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


