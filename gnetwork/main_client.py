import socket
from gclient import GClient
import sys

client = GClient()
if client.connect() == 0:
    while True:
        text = input('> ')

        if text == 'quit':
            sys.exit()
            client.clientSock.shutdown(socket.SHUT_WR)
            client.close()
            break
        client.send(text=text)