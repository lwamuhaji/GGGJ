import socket
import pickle
import threading
from . import gthread
from . import gdecorator

class GServer:

    def __init__(self, host='192.168.25.196', port=33791, buff_size=1024, encoding_format='utf-8', maxQueue=5) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host: str = host
        self.port: int = port
        self.buffer_size: int = buff_size
        self.encoding_format: str = encoding_format
        self.maxQueue: int = maxQueue

    def receive(self):
        while True:
            data: bytes = self.client_socket.recv(self.buffer_size)
            self.__handleData(data)

    def __handleData(self, data: bytes):
        data_dict: dict = pickle.loads(data)
        print(data_dict)

    def start(self) -> None:
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.maxQueue)
        self.accept()

    def startRecvThread(self):
        threading.Thread(target=self.receive, daemon=True).start()

    @gdecorator.AcceptDecorator()
    def accept(self):
        self.client_socket, self.client_address = self.server_socket.accept()

    @gdecorator.SendDecorator()
    def send(self, **kwargs):
        data = pickle.dumps(kwargs)
        self.client_socket.sendall(data)
