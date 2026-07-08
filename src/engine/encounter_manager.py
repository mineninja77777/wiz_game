from __future__ import annotations # woah time travel
from dataclasses import dataclass
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



class EncounterManager:
    _instance: EncounterManager | None = None

    entities: list[Entity] # the entities in battle

    def __init__(self):
        pass # does anything actually need to happen here tbh

    def run_encounter(self, level: int, players: list[Entity]):
        self.generate_encounter(level, players)

        # while not is_finished():
        #     pass

    
    
    def generate_encounter(self, level: int, players: list[Entity]):
        self.entities = []
        self.entities.append(*players)


        budget: int = level

        while budget > 0:
            potential: list[type] = self.get_enemies_below_level(budget)
            if len(potential) == 0: 
                break
            
            next_enemy: type = random.choice(potential)
            budget -= next_enemy().level
            self.entities.append(next_enemy())

    def is_finished(self) -> bool:
        return len(self.get_aligned(False)) == 0 or len(self.get_aligned(True)) == 0

    @staticmethod
    def get_enemies_below_level(level: int) -> list[type]:
        enemies: list[type] = []

        for enemy in _enemy_registry:
            if enemy().level <= level:
                enemies.append(enemy)
        
        return enemies
    
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


