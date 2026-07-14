from __future__ import annotations
from typing import overload
import os.path
import json
import random

from engine.events import Event


class UIManager:
    _instance: UIManager | None = None

    _data: dict[str, list[str]] | None = None

    def __init__(self) -> None:
        self.data()

    def print_event(self, event: Event) -> None:
        # json structure for prints is name: [possible msgs]
        msg: str = random.choice(self.data()[event.kind])
        for name, val in event.params.items():
            if not isinstance(val, list):
                msg = msg.replace('{' + name + '}', str(val))
                continue
            msg = msg.replace('{' + name + '}', "\n".join([str(va) for va in val]))
        print(msg)
    
    @overload
    def get_input(self, event: Event) -> str: ...

    @overload
    def get_input[T](self, event: Event, options: dict[str, T]) -> T: ...

    def get_input[T](self, event: Event, options: dict[str, T] | None = None) -> T | str:
        self.print_event(event)
        user_input: str = input()
        if options is None:
            return user_input
        while user_input not in options.keys():
            self.print_event(Event('invalid_input'))
            user_input = input()
        
        return options[user_input]
    
    @staticmethod
    def generate_options[T](options: list[T]) -> dict[str, T]:
        return {str(choice): choice for choice in options}

    def data(self) -> dict[str, list[str]]:
        if self._data is None:
            text = json.load(open(os.path.abspath("src/instances/text.JSON")))
            self._data = text["events"]
            return text
        return self._data

    @classmethod
    def instance(cls) -> UIManager:
        if cls._instance is None:
            cls._instance = UIManager()
        return cls._instance
