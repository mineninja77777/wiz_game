from __future__ import annotations # woah time travel
from typing import TYPE_CHECKING
import random


if TYPE_CHECKING:
    from engine.entity import Entity

_enemy_registry: list[type] = []


def register_enemy():
    def wrap(cls):
        _enemy_registry.append(cls)
        return cls
    return wrap


class Encounter:

    level: int # the level of the encounter

    encounter_contents: list[Entity]

    
    def __init__(self, level: int):
        self.level = level

        self.encounter_contents = []

        self.generate_encounter()

    def generate_encounter(self):
        budget: int = self.level

        while budget > 0:
            potential: list[type] = self.get_enemies_below_level(budget)
            if len(potential) == 0: 
                break
            
            next_enemy: type = random.choice(potential)
            budget -= next_enemy().level
            self.encounter_contents.append(next_enemy())
    
    @staticmethod
    def get_enemies_below_level(level: int) -> list[type]:
        enemies: list[type] = []

        for enemy in _enemy_registry:
            if enemy().level <= level:
                enemies.append(enemy)
        
        return enemies

    

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


