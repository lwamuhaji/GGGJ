import socket
import pickle

class GClient:

    def __init__(self, SRC_ADDRESS='0.0.0.0', SRC_PORT=33791, DEST_ADDRESS='218.55.184.192', DEST_PORT=33791) -> None:
        self.SRC_ADDRESS, self.SRC_PORT = SRC_ADDRESS, SRC_PORT
        self.DEST_ADDRESS, self.DEST_PORT = DEST_ADDRESS, DEST_PORT
        self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def connect(self):
        try:
            self.clientSock.bind((self.SRC_ADDRESS, self.SRC_PORT))
            self.clientSock.connect((self.DEST_ADDRESS, self.DEST_PORT))
        except Exception as e:
            print(e)
            self.clientSock.close()
            return 1
        else:
            return 0

    def send(self, **kwargs):
        try:
            data = pickle.dumps(kwargs)
            self.clientSock.sendall(data)
        except Exception as e:
            print(e)
            return 1
        else:
            return 0

    def close(self):
        self.clientSock.close()