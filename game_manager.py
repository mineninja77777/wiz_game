from __future__ import annotations # woah time travel

from encounter_manager import EncounterManager

class GameManager:
    _instance: GameManager | None = None
    
    encounter_manager: EncounterManager

    difficulty: int # the difficulty

    def __init__(self):
        self.players = []
        self.encounter_manager = EncounterManager.instance()

        self.difficulty = int(input("Difficulty: (1/2/3)"))


    def main(self):
        pass

    @classmethod
    def instance(cls) -> GameManager:
        if cls._instance is None:
            cls._instance = GameManager()
        return cls._instance