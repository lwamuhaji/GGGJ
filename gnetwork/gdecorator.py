from typing import Callable

class AcceptDecorator:
    def __call__(self, func) -> Callable[..., None]:
        def wrapper(*args, **kwargs) -> None:
            print('Waiting...')
            func(args[0])
            print('Client connected: {}'.format(args[0].client_address))
        return wrapper

class SendDecorator:
    def __call__(self, func) -> Callable[..., None]:
        def wrapper(*args, **kwargs) -> None:
            print('Begin sending')
            func(args[0], **kwargs)
            print('End sending:', kwargs)
        return wrapper

class ConnectDecorator:
    def __call__(self, func) -> Callable[..., None]:
        def wrapper(*args, **kwargs) -> None:
            print('Connecting')
            func(args[0])
            print('Connected to server')
        return wrapper

class ReceiveDecorator:
    def __call__(self, func) -> Callable[..., None]:
        def wrapper(*args, **kwargs) -> bytes:
            print('Start receiving')
            data = func(args[0])
            print('Received', data)
            return data
        return wrapper