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
            func(args[0])
            print('End sending:', kwargs)
        return wrapper