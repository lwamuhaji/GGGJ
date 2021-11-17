import socket
import pickle
import threading

class GClient:

    def __init__(self, SRC_ADDRESS='0.0.0.0', SRC_PORT=33791, DEST_ADDRESS='218.55.184.192', DEST_PORT=33791, buff_size=1024) -> None:
        self.SRC_ADDRESS, self.SRC_PORT = SRC_ADDRESS, SRC_PORT
        self.DEST_ADDRESS, self.DEST_PORT = DEST_ADDRESS, DEST_PORT
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.buffer_size = buff_size
        
    def connect(self):
        try:
            self.client_socket.bind((self.SRC_ADDRESS, self.SRC_PORT))
            self.client_socket.connect((self.DEST_ADDRESS, self.DEST_PORT))
        except Exception as e:
            print(e)
            self.client_socket.close()
            return 1
        else:
            self.__onConnected()
            return 0

    def __onConnected(self):
        receivingThread = threading.Thread(target=self.__recv)
        receivingThread.daemon = True
        receivingThread.start()

    def __recv(self):
        while True:
            try:
                recv_data = self.client_socket.recv(self.buffer_size)
            except Exception as e:
                print('error on recv:', e)
                break
            else:
                continue
                self.__handleData(recv_data)

    def __handleData(self, recv_data):
        data: dict = pickle.loads(recv_data)
        if data['header'] == 'movement':
            print(data['position'])


    def send(self, **kwargs):
        try:
            data = pickle.dumps(kwargs)
            self.client_socket.sendall(data)
        except Exception as e:
            print(e)
            return 1
        else:
            return 0

    def close(self):
        self.client_socket.close()
