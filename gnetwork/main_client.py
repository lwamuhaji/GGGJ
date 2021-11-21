if __name__ == '__main__':
    if __package__ is None:
        print(1)
        import sys
        from os import path
        print(path.dirname( path.dirname( path.abspath(__file__) ) ))
        sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))
        from gclient import GClient

print(__name__)
print(__package__)
#client = GClient()
#client.connect()
#print("Connected to Server")

#while True:
#    client.send(text=input('>'))