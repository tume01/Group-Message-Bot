import abc
from typing import Any, Dict
from bot.models import EventMessage


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, successor: Any = None):
        self._successor = successor

    def handle_request(self, request: Any):
        if self.is_valid(request):
            self.perform(request)
        elif self._successor is not None:
            self._successor.handle_request(request)

    @abc.abstractmethod
    def is_valid(self, request: Any) -> bool:
        pass

    @abc.abstractmethod
    def perform(self, request: Any) -> None:
        pass

class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class AbstractMessageFactory(metaclass=Singleton):

    def build_text_message(self, json_object: Dict[str,str]) -> EventMessage:
        pass

    def build_media_message(self, json_object: Dict[str,str]) -> EventMessage:
        pass