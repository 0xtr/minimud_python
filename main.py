import random
import selectors
import socket
import sys
import pdb

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


def accept(sock, mask):
    newsock, address = sock.accept()
    newsock.setblocking(False)
    print("connection from " + str(newsock) + " at " + str(address))
    MessageQueue.initQueue(newsock)
    selector.register(newsock, selectors.EVENT_READ, read)
    # TODO: welcome them nicely


def read(sock, mask):
    IncomingHandler.incoming_handler(sock)


# TODO: store selector in class
selector = selectors.DefaultSelector()
selector.register(listensock, selectors.EVENT_READ, accept)

while True:
    events = selector.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
