from __future__ import annotations # woah time travel
from typing import TYPE_CHECKING

import random


from action import Attack, Effect
from entity import Entity

if TYPE_CHECKING:
    from context import EncounterContext

# --------- positive -----------

class Heal(Effect):
    # will instantly expire after one tick 

    name = "Heal"

    heal: float
    overheal: bool
    percent: bool

    def __init__(self, heal: float, can_overheal: bool = False, percent: bool = False):
        """
            heal: amount healed
            can_overheal: if the hp after can be higher than the entity's max
            percent: will interpret the heal parameter as a percentage of the entity's max hp

        """

        self.heal = heal
        self.overheal = can_overheal
        self.percent = percent

    def on_apply(self, target: Entity, context: EncounterContext):
        if self.percent:
            target.hp += self.heal * target.stats.max_hp
        else:
            target.hp += self.heal
        
        if target.hp > target.stats.max_hp and not self.overheal:
            target.hp = target.stats.max_hp
    
    def expired(self, target: Entity, context: EncounterContext) -> bool:
        return True


class RecoverMana(Effect):
    # will instantly expire after one tick 

    name = "Mana Regen"

    mana_gain: float
    overmana: bool
    percent: bool

    has_acted: bool

    def __init__(self, mana_gain: float, can_overcharge: bool = False, percent: bool = False):
        self.mana_gain = mana_gain
        self.overmana = can_overcharge
        self.percent = percent

    def on_apply(self, target: Entity, context: EncounterContext):
        if self.percent:
            target.mana += self.mana_gain * target.stats.max_mana
        else:
            target.mana += self.mana_gain
        
        if target.mana > target.stats.max_mana and not self.overmana:
                target.mana = target.stats.max_mana
    
    def expired(self, target: Entity, context: EncounterContext) -> bool:
        return True


# --------- negative -----------

class DOT(Effect): 
    name: str = "Damage over time"

    turns_left: int
    damage: Attack

    def __init__(self, name: str, turns: int, damage: Attack):
        self.name = name
        self.turns_left = turns
        self.damage = damage
    
    def tick(self, target: Entity, context: EncounterContext):
        self.turns_left -= 1
        target.recieve_attack(self.damage, context)
    
    def expired(self, target: Entity, context: EncounterContext) -> bool:
        return self.turns_left <= 0


class Stun(Effect):
    name: str = "Stun"
    
    def __init__(self, turns: int):
        self.turns_left = turns

    def tick(self, target: Entity, context: EncounterContext) -> None:
        self.turns_left -= 1

    def blocks_turn(self, target: Entity, context: EncounterContext) -> bool:
        return True

    def expired(self, target: Entity, context: EncounterContext) -> bool:
        return self.turns_left <= 0

class Prone(Effect):
    name: str = "Prone"

    old_dodge: float
    
    def __init__(self):
        pass

    def on_apply(self, target: Entity, context: EncounterContext):
        self.old_dodge = target.stats.dodge
        target.stats.dodge = 0

    def blocks_turn(self, target: Entity, context: EncounterContext) -> bool:
        return True

    def expired(self, target: Entity, context: EncounterContext) -> bool:
        return True
    
    def remove(self, target: Entity, context: EncounterContext):
        target.stats.dodge = self.old_dodge
        return super().remove(target, context)


class Realign(Effect): # works weird but yk whatever
    name: str = "Realign"

    level: int # the level of the enemy which would be unable to resist

    new_alignment: bool
    old_alignment: bool

    def __init__(self, new_alignment: bool, level: int):
        self.level = level
        self.new_alignment = new_alignment
        self.old_alignment = new_alignment
    
    def on_apply(self, target: Entity, context: EncounterContext):
        if target.aligned != self.new_alignment:
            self.old_alignment = target.aligned
            target.aligned = self.new_alignment

    def expired(self, target: Entity, context: EncounterContext) -> bool:
        if target.level > self.level:
            return True
        elif random.random() * target.level > self.level:
            return True
        return False
    
    def remove(self, target: Entity, context: EncounterContext):
        target.aligned = self.old_alignment
        super().remove(target, context)


class HPMaxReduction(Effect): # works weird but yk whatever
    name: str = "Life Drain"

    reduction: float


    def __init__(self, reduction: float):
        self.reduction = reduction
    
    def on_apply(self, target: Entity, context: EncounterContext):
        target.stats.max_hp -= self.reduction

    def expired(self, target: Entity, context: EncounterContext) -> bool:
        return False

    def remove(self, target: Entity, context: EncounterContext):
        target.stats.max_hp += self.reduction
        super().remove(target, context)

# --------------------------- who knows ----------------------

class SummonEffect(Effect):
    name: str = "Summon"
    
    summonee: Entity

    def __init__(self, summonee: Entity):
        self.summonee = summonee
        
    def on_apply(self, target: Entity, context: EncounterContext):
        context.add_entity(self.summonee)

    def expired(self, target: Entity, context: EncounterContext) -> bool:
        return True