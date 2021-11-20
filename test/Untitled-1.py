class Decorator:
    def __init__(self, a) -> None:
        pass

    def __call__(self, original_func):
        def wrapper(*args, **kwargs):
            original_func(*args, **kwargs)
        return wrapper
 
class Bar:
    @Decorator
    def foo(self):
        print('im foo')

b = Bar()
b.foo()