import random
import socket
import sys
import select

# get a suitable port
from src.sqlitehelper import SQLiteHelper

port = random.randint(5000, 6000)
print("Use port " + str(port) + " for connections\n")

# open the sqlite3 dbs
dbManager = SQLiteHelper.SQLDBConnector()
assert dbManager.connectedToAllDatabases

# create the master socket
listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen.setblocking(0)

# bind it to our chosen port
try:
    listen.bind(("None", port))
except Exception as e:
    print(e.args)
    sys.exit(1)

# set listener for connections
if listen.listen() != 0:
    print("Listening for connections failed")
    sys.exit(1)

iterate = True
inputs = [listen]
outputs = []
error = []

while iterate:
    print("loop go")
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
        break

print("minimud server exited")
sys.exit(1)
