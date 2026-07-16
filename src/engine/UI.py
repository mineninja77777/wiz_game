from __future__ import annotations
from typing import overload
from collections.abc import Callable
import os.path
import json
import random

from engine.events import Event


class UIManager:
    _data: dict[str, list[str]] | None = None

    def __init__(self) -> None:
        raise Exception("nope")

    @classmethod
    def print_event(cls, event: Event, new_line: bool = True) -> None:
        # json structure for prints is name: [possible msgs]
        a = cls.data()
        msg: str = random.choice(cls.data()[event.kind])
        for name, val in event.params.items():
            if not isinstance(val, list):
                msg = msg.replace('{' + name + '}', str(val))
                continue
            msg = msg.replace('{' + name + '}', "\n".join([str(va) for va in val]))
        print(msg)
        if new_line:
            print("")
    
    @classmethod
    @overload
    def get_input(cls, event: Event) -> str: ...

    @classmethod
    @overload
    def get_input[T](cls, event: Event, options: dict[str, T]) -> T: ...

    @classmethod
    def get_input[T](cls, event: Event, options: dict[str, T] | None = None) -> T | str:
        cls.print_event(event, new_line=False)
        user_input: str = input()
        if options is None:
            return user_input
        while user_input not in options.keys():
            cls.print_event(Event('invalid_input'), new_line=False)
            user_input = input()
        print("")
        return options[user_input]
    
    @staticmethod
    def generate_options[T](options: list[T], str_func: Callable[[T], str] | None = None) -> dict[str, T]:
        if str_func is None:
            return {str(choice): choice for choice in options}
        return {str_func(choice): choice for choice in options}
    
    @classmethod
    def data(cls) -> dict[str, list[str]]:
        if cls._data is None:
            text = json.load(open(os.path.abspath("src/instances/text.JSON")))
            cls._data = text["events"]
            return text["events"]
        return cls._data