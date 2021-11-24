import threading
import pickle
import gnetwork.gdecorator as gdecorator

class AcceptThread(threading.Thread):
    def __init__(self, server) -> None:
        super().__init__()
        self.setServer(server)

    def setServer(self, server):
        from . import gserver
        self.server: gserver.GServer = server

    def run(self) -> None:
        self.client_socket, self.client_address = self.server.server_socket.accept()
        print('Client connected: {}'.format(self.client_address))

class ReceiveThread(threading.Thread):
    def __init__(self, intent, daemon=True) -> None:
        super().__init__()
        import gnetwork.gserver as gserver
        self.intent: gserver.GServer = intent

    def run(self) -> None:
        print('Receive thread started')
        while True:
            data = self.receive()

    @gdecorator.ReceiveDecorator()
    def receive(self) -> bytes:
        return self.intent.client_socket.recv(self.intent.buffer_size)

    def handleData(self, data: bytes):
        data_dict: dict = pickle.loads(data)
        print(data_dict)
        
class GServerThread(threading.Thread):
    
    def __init__(self, server) -> None:
        super().__init__()
        from gnetwork.gserver import GServer
        self.server: GServer = server

    def run(self) -> None:
        self.client_socket, self.client_address = self.server.server_socket.accept()
        self.__onAccepted()

    def __onAccepted(self) -> None:
        self.server.startNewThread()
        self.__receiveFromClient()
        print('Client connected: {}'.format(self.client_address))

    def __receiveFromClient(self) -> None:
        receivingThread = threading.Thread(target=self.__recv)
        receivingThread.daemon = True
        receivingThread.start()

    def __recv(self) -> None:
        while True:
            try:
                recv_data = self.client_socket.recv(self.server.buffer_size)
            except Exception as e:
                print('error on recv:', e)
                break
            else:
                self.__handleData(recv_data)

    def __handleData(self, recv_data: bytes):
        data: dict = pickle.loads(recv_data)
        if data['header'] == 'movement':
            print(data['position'])

    def send(self, data: str) -> int:
        try:
            self.client_socket.send(data.encode(self.server.encoding_format))
        except AttributeError as e:
            pass
        except Exception as e:
            print('error on send:', e)
            return 1
        else:
            return 0

    def log(self, *args):
        print(self.client_address, args)