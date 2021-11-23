from gserver import GServer

server = GServer()
server.start()
server.startRecvThread()

while True:
    server.send(text=input('>'))