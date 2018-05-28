import random
import socket
import sys
import sqlite
import utils

from sqlite_util import *
from util import *

# get a suitable port
port = random.randint(5000, 6000)
print "Use port %d for connections\n", port

# open the sqlite3 dbs
assert sqlite_util.init_dbs() == sys.EXIT_SUCCESS

# create the master socket
listen_socket = socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setblocking(0)

# bind it to our chosen port
try: 
    socket.bind(listen_socket, '')
except Exception e:
    print e.args
    sys.exit(sys.EXIT_FAILURE)

# set listener for connections
if socket.listen(listen_socket, SOMAXCONN) != 0:
    print "Listening for connections failed"
    sys.exit(sys.EXIT_FAILURE)

iterate = True
inputs = [listen_socket]
outputs = []

while (iterate):
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

print "minimud server exited"
sys.exit(sys.EXIT_FAILURE)