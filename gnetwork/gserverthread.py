import threading
import pickle

class GServerThread(threading.Thread):
    
    def __init__(self, server) -> None:
        super().__init__()
        from gnetwork.gserver import GServer
        self.server: GServer = server

    def run(self) -> None:
        try:
            self.client_socket, self.client_address = self.server.server_socket.accept()
        except Exception as e:
            print('accept failed:', e)
            self.server.server_socket.close()
        else:
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
                data = pickle.loads(recv_data)
            except Exception as e:
                print('error on recv:', e)
                break
            else:
                print(data['pos'])
                #print(str(self.client_address[0]) + ': ' + data['text'])

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