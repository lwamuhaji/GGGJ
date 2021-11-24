if __name__ == '__main__':
    import os, sys
    mypath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(mypath)
    if not mypath in sys.path: sys.path.append(mypath)

from gnetwork.gclient import GClient

client = GClient()
client.connect()
client.startRecvThread()

while True:
    client.send(text=input('>'))