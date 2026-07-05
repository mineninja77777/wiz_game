from __future__ import annotations # woah time travel

from base import Action_Type, Attack_Type
from action import Action, Attack, Effect
from entity import Entity
from encounter_manager import Encounter

class GameManager:
    _instance: GameManager | None = None

    difficulty: int # the difficulty

    def __init__(self):
        self.players = []
        self.difficulty = int(input("Difficulty: (1/2/3)")) # placeholder

        

    def main(self):
        pass

    @classmethod
    def instance(cls) -> GameManager:
        if cls._instance is None:
            cls._instance = GameManager()
        return cls._instance