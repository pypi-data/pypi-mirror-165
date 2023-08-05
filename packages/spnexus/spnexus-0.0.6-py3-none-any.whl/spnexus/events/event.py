from src.lib.autobot.base import Base
from src.lib.autobot.events.exceptions import *


class Event(Base):

    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        if handler is None:
            raise NoValue
        if not hasattr(handler, '__call__'):
            raise NotCallable
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        if handler is None:
            raise NoValue
        if not hasattr(handler, '__call__'):
            raise NotCallable
        self.__handlers.remove(handler)
        return self

    def __len__(self):
        return len(self.__handlers) if isinstance(self.__handlers, list) else 0

    def __call__(self, *args, **kwargs):
        for handler in self.__handlers:
            handler(*args, **kwargs)

    def __str__(self):
        return f'{self.__module__}.{self.__class__.__name__}'
