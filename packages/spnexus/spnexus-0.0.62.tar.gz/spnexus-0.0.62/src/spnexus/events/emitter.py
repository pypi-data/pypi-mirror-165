from .event import Event


class Emitter(object):
    __handler_map: dict = {}

    def on(self, event):
        from .exceptions import InvalidEvent

        def handler_decorator(handler) -> bool:
            from .exceptions import InvalidHandler

            if handler is None or not hasattr(handler, '__call__'):
                raise InvalidHandler

            if isinstance(event, list):
                outcome = True

                for item in event:
                    if item is None or not issubclass(item, Event):
                        raise InvalidEvent

                    if not self.add_listener(item, handler):
                        outcome = False

                return outcome

            if event is None or not issubclass(event, Event):
                raise InvalidEvent

            return self.add_listener(event, handler)

        return handler_decorator

    def add_listener(self, event, handler) -> bool:
        self.__setup_handler_map()
        event_type = f'{event.__module__}.{event.__name__}' if issubclass(event, Event) else str(event)

        if event_type not in self.__handler_map:
            self.__handler_map[event_type] = Event()

        self.__handler_map[event_type] += handler

        return True

    def remove_listener(self, event, handler) -> bool:
        self.__setup_handler_map()
        event_type = str(event)

        if event_type not in self.__handler_map:
            return False

        self.__handler_map[event_type] -= handler

    def __setup_handler_map(self):
        if self.__handler_map is None:
            self.__handler_map = {}

        if not isinstance(self.__handler_map, dict):
            self.__handler_map = dict(self.__handler_map)

    def emit(self, event: str or Event = None) -> bool:
        event_type = str(event)
        if not self.has_event(event_type):
            return False
        self.__handler_map[event_type](event)
        if hasattr(super(), 'emit') and hasattr(super().emit, '__call__'):
            super().emit(event)
        return True

    def has_event(self, event: str or Event) -> bool:
        event_type = str(event)
        return isinstance(self.__handler_map, dict) and event_type in self.__handler_map \
               and issubclass(self.__handler_map[event_type].__class__, Event)
