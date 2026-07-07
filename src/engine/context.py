from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine.encounter_manager import EncounterManager
    from engine.entity import Entity


class EncounterContext:
    _entities: list[Entity]

    def add_entity(self, entity: Entity):
        self._entities.append(entity)

    def remove_entity(self, entity: Entity):
        self._entities.remove(entity)

    def get_aligned(self, alignment: bool) -> list[Entity]:
        result = []
        for entity in self._entities:
            if entity.aligned == alignment:
                result.append(entity)
        return result
    
    def entities(self) -> list[Entity]:
        return self._entities.copy()