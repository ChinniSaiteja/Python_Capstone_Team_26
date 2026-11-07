from collections.abc import Iterable, Iterator

from .recognition_event import RecognitionEvent


class EventGenerator(Iterator[RecognitionEvent]):
    """
    Iterator that consumes recognition events one at a time.

    This simulates a real-time stream of recognition events.
    """

    def __init__(self, events: Iterable[RecognitionEvent]):
        self.__events = list(events)
        self.__index = 0
        self.__initialized = False

    def initialize(self) -> None:
        self.__index = 0
        self.__initialized = True

    @property
    def initialized(self) -> bool:
        return self.__initialized

    @property
    def index(self) -> int:
        return self.__index

    def __iter__(self):
        return self

    def __next__(self) -> RecognitionEvent:
        if self.__index >= len(self.__events):
            raise StopIteration

        event = self.__events[self.__index]
        self.__index += 1

        return event

    def reset(self) -> None:
        self.__index = 0

    def __len__(self) -> int:
        return len(self.__events)