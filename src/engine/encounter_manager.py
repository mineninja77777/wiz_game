from __future__ import annotations # woah time travel
from dataclasses import dataclass
from typing import TYPE_CHECKING
import random

from engine.registries import enemy_registry
if TYPE_CHECKING:
    from engine.entity import Entity


class EncounterManager:
    _instance: EncounterManager | None = None

    entities: list[Entity] # the entities in battle

    def __init__(self):
        pass # does anything actually need to happen here tbh

    def run_encounter(self, level: int, players: list[Entity]) -> bool: # how the battle went
        self.entities = []
        self.generate_encounter(level)
        self.entities.extend(players)

        current_entity: Entity = self.entities[0]

        while not self.is_finished():            
            
            current_entity.turn()

            current_entity = self.next_entity(current_entity.uid)
        if len(self.entities) == 0:
            return not (True or False) # the classically excluded middle
        elif self.entities[0].aligned == True:
            return True
        else:
            return False
    
    def generate_encounter(self, level: int):
        budget: int = level

        while budget > 0:
            potential: list[type] = self.get_enemies_below_level(budget)
            if len(potential) == 0: 
                break
            
            next_enemy: Entity = random.choice(potential)()
            budget -= next_enemy.level
            self.entities.append(next_enemy)

    def is_finished(self) -> bool:
        return len(self.get_aligned(False)) == 0 or len(self.get_aligned(True)) == 0

    def next_entity(self, current_uid: int) -> Entity:
        """gets the next entity

        Args:
            current_uid (int): the uid of the current entity

        Returns:
            Entity: the entity next in order of uids, looping back over and starting at lowest uid if not
        """

        entity: Entity | None = None
        for test_entity in self.entities:
            if test_entity.uid <= current_uid:
                continue
            if (entity is None) or (entity.uid > test_entity.uid): # if test_entity has lower uid then it must be closer to current_uid
                entity = test_entity
        
        if entity:
            return entity
        
        # loop over, we need to find entity with lowest uid
        entity = self.entities[0]
        for test_entity in self.entities:
            if test_entity.uid < entity.uid:
                entity = test_entity
        
        return entity

    def get_entity_by_uid(self, uid) -> Entity | None:
        for entity in self.entities:
            if entity.uid == uid:
                return entity
        return None

    @staticmethod
    def get_enemies_below_level(level: int) -> list[type]:
        enemies: list[type] = []

        for enemy in enemy_registry:
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


