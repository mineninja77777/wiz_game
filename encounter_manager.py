from __future__ import annotations # woah time travel
from typing import TYPE_CHECKING
import inspect

from base import Action_Type, Attack_Type
from action import Action, Attack, Effect

if TYPE_CHECKING:
    from entity import Entity

import instances.entities


class Encounter:

    level: int # the level of the encounter

    encounter_contents: list[Entity]

    
    def __init__(self, level: int):
        self.level = level

        self.generate_encounter()

    def generate_encounter(self):
        budget: int = self.level

        while budget > 0:
            pass

    

class EncounterManager:
    _instance: EncounterManager | None = None

    current_encounter: Encounter

    entities: list[Entity] # the entities in battle


    def get_aligned(self, alignment: bool) -> list[Entity]:
        result = []
        for entity in self.entities:
            if entity.aligned == alignment:
                result.append(entity)
        return result
    
    @classmethod
    def instance(cls) -> EncounterManager:
        if cls._instance is None:
            cls._instance = EncounterManager()
        return cls._instance


