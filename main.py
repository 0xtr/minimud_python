import random
import socket
import sys
import select
import pdb

# get a suitable port
from asyncio import Queue

from src.io import IncomingHandler
from src.io.MessageQueue import MessageQueue
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
        for item in inputs:
            if item is listensock:
                newsock, address = item.accept()
                print("connection from " + str(newsock) + " at " + address)
                newsock.setblocking(0)
                inputs.append(newsock)
                MessageQueue.initQueue(newsock)
            else:
                IncomingHandler.incoming_handler(item.fileno())
                # check message queue next

    if outputs:
        print("uh oh")
        print(len(outputs))

print("minimud server exited")
sys.exit(1)
