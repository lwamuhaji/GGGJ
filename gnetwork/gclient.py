import socket
import pickle
import gnetwork.gthread as gthread
import gnetwork.gdecorator as gdecorator

class GClient:

    def __init__(self, SRC_ADDRESS='0.0.0.0', SRC_PORT=33791, DEST_ADDRESS='218.55.184.192', DEST_PORT=33791, buff_size=1024) -> None:
        self.SRC_ADDRESS, self.SRC_PORT = SRC_ADDRESS, SRC_PORT
        self.DEST_ADDRESS, self.DEST_PORT = DEST_ADDRESS, DEST_PORT
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.buffer_size = buff_size

    def startRecvThread(self):
        gthread.ReceiveThread(self).start()

    @gdecorator.ConnectDecorator()
    def connect(self):
        self.client_socket.bind((self.SRC_ADDRESS, self.SRC_PORT))
        self.client_socket.connect((self.DEST_ADDRESS, self.DEST_PORT))

    @gdecorator.SendDecorator()
    def send(self, **kwargs):
        self.client_socket.sendall(pickle.dumps(kwargs))
    
    #@gdecorator.SendDecorator()
    def sendPosition(self, position):
        data = pickle.dumps(position)
        self.client_socket.sendall(data)

    #@gdecorator.SendDecorator()
    def sendScore(self, score):
        data = pickle.dumps(score)
        self.client_socket.sendall(data)

    def close(self):
        self.client_socket.close()
