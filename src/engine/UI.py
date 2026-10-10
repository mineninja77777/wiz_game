from __future__ import annotations
from typing import overload
from collections.abc import Callable
import os.path
import json
from typing import cast

from engine.events import Event
from engine.registries import dialogue_funcs_registry

class UIManager:
    _data: dict[str, str | dict] | None = None

    def __init__(self) -> None:
        raise Exception("nope")

    @classmethod
    def print_event(cls, event: Event, new_line: bool = True) -> None:
        event_data: str | dict = cls.data()[event.kind]
        msg: str
        if isinstance(event_data, str):
            msg = event_data
        elif isinstance(event_data, dict):
            # validation
            keys: list[str] = list(event_data.keys())
            if not ("function" in keys and "params" in keys):
                raise KeyError(f"JSON is poorly structured in dialogue.JSON, under {event.kind}")

            # doing everything ever
            msg = dialogue_funcs_registry[UIManager.replace_in_str(event_data["function"], event.params)](UIManager.traverse_and_replace(event_data["params"], event.params))

        msg = UIManager.replace_in_str(msg, event.params)
        print(msg)
        if new_line:
            print("")

    @staticmethod
    def replace_in_str(x: str, values: dict[str, object]) -> str:
        new = x
        for name, value in values.items():
            if isinstance(value, list):
                new = new.replace('{' + name + '}', "\n".join([val for val in value]))
            else:
                new = new.replace('{' + name + '}', str(value))
        return new

    @staticmethod
    def traverse_and_replace[T: (str, int, list, dict)](x: T, values: dict[str, object]) -> T:
        if isinstance(x, str):
            return UIManager.replace_in_str(x, values)
        elif isinstance(x, int):
            return x
        elif isinstance(x, list):
            new = []
            for val in x:
                new.append(UIManager.traverse_and_replace(val, values))
            return cast(T, new)
        elif isinstance(x, dict):
            new = {}
            for key, element in x.items():
                new[UIManager.traverse_and_replace(key, values)] = UIManager.traverse_and_replace(element, values)
            return cast(T, new)
        else:
            raise TypeError(f"JSON is poorly formatted in dialogue.json, \n {x} is wrong type")


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
    def data(cls) -> dict[str, str | dict]:
        if cls._data is None:
            text = json.load(open(os.path.abspath("src/instances/dialogue.JSON")))
            cls._data = text["events"]
            return text["events"]
        return cls._data