import socket
from typing import List
import gserverthread

class GServer:

    def __init__(self, host='192.168.25.196', port=33791, buff_size=1024, encoding_format='utf-8', maxQueue=5) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.threads: List[gserverthread.GServerThread] = list()
        self.host: str = host
        self.port: int = port
        self.buffer_size: int = buff_size
        self.encoding_format: str = encoding_format
        self.maxQueue: int = maxQueue

    def start(self) -> None:
        try:
            self.server_socket.bind((self.host, self.port))
        except Exception as e:
            print('bind failed:', e)
            self.server_socket.close()
            print('closed server socket')
        else:
            self.__beginListen()

    def __beginListen(self) -> None:
        try:
            self.server_socket.listen(self.maxQueue)
        except Exception as e:
            print('listen failed:', e)
            self.server_socket.close()
            print('closed server socket')
        else:
            self.startNewThread()
            self.__loop()

    def __loop(self) -> None:
        while True:
            for thread in self.threads:
                if thread.send('test') != 0:
                    self.threads.remove(thread)

    def startNewThread(self) -> None:
        thread = gserverthread.GServerThread(self)
        self.threads.append(thread)
        thread.daemon = True
        thread.start()
