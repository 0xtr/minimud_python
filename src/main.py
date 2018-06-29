import random
import socket
import sys
import select

from . import sqlite_custom as sql

# get a suitable port
port = random.randint(5000, 6000)
print("Use port %d for connections\n", port)

# open the sqlite3 dbs
dbManager = sql.SQLDBManager()
assert dbManager.init_dbs() == 0

# create the master socket
listen_socket = socket(socket.AF_INET, socket.SOCK_STREAM)
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
exceptional = []

while iterate:
    try:
        inputs, outputs, exceptional = select.select(inputs, outputs, [])
    except select.error as selError:
        break
    except socket.error as sockError:
        break

    if (inputs):
        print("hello: " + len(inputs))
        break;

print("minimud server exited")
sys.exit(1)
