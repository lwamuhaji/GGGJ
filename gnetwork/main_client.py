import socket
from gclient import GClient
import sys

pos = (0, 0)

client = GClient()

if client.connect() == 0:
    print("Connected to Server")
    while True:
        text = input('> ')

        if text == 'quit':
            sys.exit()
            client.clientSock.shutdown(socket.SHUT_WR)
            client.close()
            break

        client.send(header='movement', position=pos)