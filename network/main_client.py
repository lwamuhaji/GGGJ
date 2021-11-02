from socket import *

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.bind(('0.0.0.0', 33791))
clientSock.connect(('218.55.184.192', 33791))