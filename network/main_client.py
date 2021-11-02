from gclient import GClient

client = GClient()
if client.connect() == 0:
    while True:
        text = input('>')

        if text == 'quit':
            break
        client.send(text=text)

client.close()