from __future__ import annotations # woah time travel

from engine.base import Action_Type, Attack_Type
from engine.action import Action, Attack, Effect
from engine.entity import Entity

from instances.effects import *

class Rest(Action): # regen some mana

    def __init__(self, level: int):
        super().__init__(
            name = "Rest",
            level = level,
            action_type = Action_Type.OTHER,
            attacks = [],
            target_effects = [],
            self_effects = [Heal(level * 5), RecoverMana(level * 2)],
            mana_cost = 0,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        self.mana_cost -= 5