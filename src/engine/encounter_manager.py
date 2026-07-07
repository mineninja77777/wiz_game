from __future__ import annotations # woah time travel
from typing import TYPE_CHECKING
import inspect

from engine.context import EncounterContext

import instances.entities

if TYPE_CHECKING:
    from engine.entity import Entity


class EncounterManager:
    _instance: EncounterManager | None = None

    context: EncounterContext


    
    
    @classmethod
    def instance(cls) -> EncounterManager:
        if cls._instance is None:
            cls._instance = EncounterManager()
        return cls._instance


