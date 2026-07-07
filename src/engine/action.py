from __future__ import annotations

from dataclasses import dataclass
from typing import overload, TYPE_CHECKING
import random

from engine.base import Attack_Type, Action_Type

if TYPE_CHECKING:
    from engine.entity import Entity
    from engine.context import EncounterContext

@dataclass
class Attack:
    """ an attack -- damage dealt to some targets, no funni business """
    dmg: float
    spread: float
    dmg_type: Attack_Type

    aoe: int # how many enemies can be affected by this -- the player does not choose which

    def get_damage(self) -> float:
        return round((random.random()-0.5) * 2.0 * self.spread + self.dmg, 1)


class Effect: # can be positive or negative
    name: str = "Effect"

    def on_apply(self, target: "Entity", context: EncounterContext):
        pass

    def tick(self, target: "Entity", context: EncounterContext):
        pass

    def blocks_turn(self, target: "Entity", context: EncounterContext) -> bool:
        return False
    
    def expired(self, target: "Entity", context: EncounterContext) -> bool:
        self.remove(target, context)
        return True
    
    def remove(self, target: "Entity", context: EncounterContext):
        target.active_effects.remove(self)


@dataclass(kw_only = True)
class Action:
    name: str
    level: int # doesn't affect stats, is only tracking how many times has been levelled
    action_type: Action_Type

    attacks: list[Attack] # attacks dealt -- the player can choose primary targets for these
    target_effects: list[Effect] # effects inflicted, are applied to each recipient of attacks

    self_effects: list[Effect]
    
    mana_cost: float # technically a self effect but ehh

    max_level: int # max level before upgrading
    upgrades: list[type]

    def level_up(self):
        self.level += 1



@overload
def enough_mana(action: Action, mana: float) -> bool: ...
    
@overload
def enough_mana(action: list[Action], mana: float) -> list[Action]: ...

def enough_mana(action: Action | list[Action], mana: float) -> bool | list[Action]:
    if type(action) == Action:
        return action.mana_cost <= mana
    
    elif type(action) == list: # technically not rigourous enough but hopefully I won't misuse it
        enough: list[Action] = []
        for spl in action:
            if spl.mana_cost <= mana:
                enough.append(spl)
        return enough
    
    else:
        raise Exception("pretty no bueno I would say")