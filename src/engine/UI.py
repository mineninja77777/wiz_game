from __future__ import annotations
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
        msg: str = random.choice(self.data()[event.kind])
        for name, val in event.params.items():
            msg = msg.replace('{' + name + '}', str(val))
        print(msg)

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
