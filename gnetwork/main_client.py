from gclient import GClient

client = GClient()
client.connect()
client.startRecvThread()

while True:
    client.send(text=input('>'))