import random
import socket
import sys
import select

# get a suitable port
from src import sqlitehelper

port = random.randint(5000, 6000)
print("Use port " + str(port) + " for connections\n")

# open the sqlite3 dbs
dbManager = sqlitehelper.SQLDBManager()
assert dbManager.init_dbs() == 0

# create the master socket
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setblocking(0)

# bind it to our chosen port
try:
    socket.bind(listen_socket, '')
except Exception as e:
    print(e.args)
    sys.exit(1)

# set listener for connections
if socket.listen() != 0:
    print("Listening for connections failed")
    sys.exit(1)

iterate = True
inputs = [listen_socket]
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
        print("hello: " + len(inputs))
        break

print("minimud server exited")
sys.exit(1)
