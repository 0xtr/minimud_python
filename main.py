import random
import socket
import sys
import select
import pdb

# get a suitable port
from src.io import IncomingHandler
from src.sqlitehelper import SQLiteHelper

# debugging
# pdb.set_trace()

port = random.randint(5000, 6000)
print("Use port " + str(port) + " for connections\n")

# open the sqlite3 dbs
dbManager = SQLiteHelper.SQLDBConnector()
assert dbManager.connectedToAllDatabases

# create the master socket
listensock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listensock.setblocking(0)

# bind it to our chosen port
try:
    listensock.bind(("", port))
except Exception as e:
    print(e.args)
    sys.exit(1)

# set listener for connections
listensock.listen()

iterate = True
inputs = [listensock]
outputs = []
error = []

while iterate:
    try:
        inputs, outputs, error = select.select(inputs, outputs, error)
    except select.error as selError:
        print(selError)
        break
    except socket.error as sockError:
        print(sockError)
        break

    if inputs:
        print("hello: " + str(len(inputs)))
        obj = inputs[0]
        for item in inputs:
            IncomingHandler.incoming_handler(item.fileno())

    if outputs:
        print("uh oh")

print("minimud server exited")
sys.exit(1)
