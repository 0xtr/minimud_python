import random
import socket
import sys
import sqlite3
import utils

from . import sqlite_custom
from . import util_custom

# get a suitable port
port = random.randint(5000, 6000)
print("Use port %d for connections\n", port)

# open the sqlite3 dbs
assert sqlite_custom.init_dbs() == 0

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
if socket.listen(listen_socket, SOMAXCONN) != 0:
    print("Listening for connections failed")
    sys.exit(1)

iterate = True
inputs = [listen_socket]
outputs = []

while (iterate):
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

print("minimud server exited")
sys.exit(1)