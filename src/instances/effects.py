import random
from typing import TYPE_CHECKING

from engine.base import Attack_Type
from engine.action import Attack, Effect
from engine.entity import Entity

from engine.encounter_manager import EncounterManager

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

    def on_apply(self, target: Entity):
        if self.percent:
            target.hp += self.heal * target.stats.max_hp
        else:
            target.hp += self.heal
        
        if target.hp > target.stats.max_hp and not self.overheal:
            target.hp = target.stats.max_hp
    
    def expired(self, target: Entity) -> bool:
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

    def on_apply(self, target: "Entity"):
        if self.percent:
            target.mana += self.mana_gain * target.stats.max_mana
        else:
            target.mana += self.mana_gain
        
        if target.mana > target.stats.max_mana and not self.overmana:
                target.mana = target.stats.max_mana
    
    def expired(self, target: Entity) -> bool:
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
    
    def tick(self, target: Entity):
        self.turns_left -= 1
        target.recieve_attack(self.damage)
    
    def expired(self, target: Entity) -> bool:
        return self.turns_left <= 0


class Stun(Effect):
    name: str = "Stun"
    
    def __init__(self, turns: int):
        self.turns_left = turns

    def tick(self, target: Entity) -> None:
        self.turns_left -= 1

    def blocks_turn(self, target: Entity) -> bool:
        return True

    def expired(self, target: Entity) -> bool:
        return self.turns_left <= 0

class Prone(Effect):
    name: str = "Prone"

    old_dodge: float
    
    def __init__(self):
        pass

    def on_apply(self, target: Entity):
        self.old_dodge = target.stats.dodge
        target.stats.dodge = 0

    def blocks_turn(self, target: Entity) -> bool:
        return True

    def expired(self, target: Entity) -> bool:
        return True
    
    def remove(self, target: Entity):
        target.stats.dodge = self.old_dodge
        return super().remove(target)


class Realign(Effect): # works weird but yk whatever
    name: str = "Realign"

    level: int # the level of the enemy which would be unable to resist

    new_alignment: bool
    old_alignment: bool

    def __init__(self, new_alignment: bool, level: int):
        self.level = level
        self.new_alignment = new_alignment
        self.old_alignment = new_alignment
    
    def on_apply(self, target: Entity):
        if target.aligned != self.new_alignment:
            self.old_alignment = target.aligned
            target.aligned = self.new_alignment

    def expired(self, target: Entity) -> bool:
        if target.level > self.level:
            return True
        elif random.random() * target.level > self.level:
            return True
        return False
    
    def remove(self, target: Entity):
        target.aligned = self.old_alignment
        super().remove(target)


class HPMaxReduction(Effect): # works weird but yk whatever
    name: str = "Friend"

    reduction: float


    def __init__(self, reduction: float):
        self.reduction = reduction
    
    def on_apply(self, target: Entity):
        target.stats.max_hp -= self.reduction

    def expired(self, target: Entity) -> bool:
        return False

    def remove(self, target: Entity):
        target.stats.max_hp += self.reduction
        super().remove(target)

# --------------------------- who knows ----------------------

class SummonEffect(Effect):
    name: str = "Summon"
    
    summonee: Entity

    def __init__(self, summonee: Entity):
        self.summonee = summonee
        
    def on_apply(self, target: Entity):
        EncounterManager.instance().entities.append(self.summonee)

    def expired(self, target: Entity) -> bool:
        return True