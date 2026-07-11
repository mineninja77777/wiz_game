from __future__ import annotations
from typing import Any # woah time travel

from engine.base import Action_Type, Attack_Type
from engine.action import Action, Attack, Effect
from engine.entity import Entity
from engine.registries import register_action

from instances.effects import *

@register_action
class Sword(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Sword", 
            level = level, 
            action_type = Action_Type.WEAPON, 
            attacks = [Attack(3 + 2*level, 1, Attack_Type.SHARP, 2)], 
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = 10,
            upgrades = [Longsword]
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 2

@register_action
class Longsword(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Longsword", 
            level = level, 
            action_type = Action_Type.WEAPON, 
            attacks = [Attack(3 + 3*level, 1, Attack_Type.SHARP, 2)], 
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 3

@register_action
class Broadsword(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Broadsword", 
            level = level, 
            action_type = Action_Type.WEAPON, 
            attacks = [Attack(3 + 2*level, 1, Attack_Type.SHARP, 5)], 
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 2


@register_action
class Mace(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Mace", 
            level = level, 
            action_type = Action_Type.WEAPON, 
            attacks = [Attack(4 + 3*level, 2, Attack_Type.BLUDGEON, 1)], 
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = 10,
            upgrades = [WindMace]
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 3

@register_action
class WindMace(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Wind Mace", 
            level = level, 
            action_type = Action_Type.WEAPON, 
            attacks = [Attack(4 + 3*level, 2, Attack_Type.BLUDGEON, 3)], 
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 3


@register_action
class Axe(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Axe",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(4 + 3*level, 2, Attack_Type.SHARP, 1)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = 10,
            upgrades = [FireAxe, BattleAxe]
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 3

@register_action
class FireAxe(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Axe",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(4 + 3*level, 2, Attack_Type.SHARP, 1)],
            target_effects = [DOT("Burn", 3, Attack(level * 2, 1, Attack_Type.FIRE, 1))], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 3
        if isinstance(self.target_effects[0], DOT):
            self.target_effects[0].damage.dmg += 2

@register_action
class BattleAxe(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Axe",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(6 + 3*level, 2, Attack_Type.SHARP, 3)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 3


@register_action
class Daggers(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Daggers",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(2 + level * 0.5, 1, Attack_Type.SHARP, 1), Attack(2 + level * 0.5, 1, Attack_Type.SHARP, 1)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = 10,
            upgrades = [FrostDaggers, BloodDaggers]
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 0.5
        self.attacks[1].dmg += 0.5

@register_action
class FrostDaggers(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Daggers",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(2 + level * 0.5, 1, Attack_Type.SHARP, 1), Attack(2 + level * 0.5, 1, Attack_Type.SHARP, 1)],
            target_effects = [Stun(1)], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 0.5
        self.attacks[1].dmg += 0.5

@register_action
class BloodDaggers(Action):
    
    def __init__(self, level: int):
        super().__init__(
            name = "Daggers",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(2 + level * 0.5, 1, Attack_Type.SHARP, 1), Attack(2 + level * 0.5, 1, Attack_Type.SHARP, 1)],
            target_effects = [], 
            self_effects = [Heal(level)],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 0.5
        self.attacks[1].dmg += 0.5
        if isinstance(self.self_effects[0], Heal):
            self.self_effects[0].heal += 1


@register_action
class Staff(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Staff",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(3 + level, 1, Attack_Type.BLUDGEON, 1)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = 10,
            upgrades = [EssenceStaff]
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 1

@register_action
class EssenceStaff(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Staff",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(3 + level, 1, Attack_Type.BLUDGEON, 1)],
            target_effects = [], 
            self_effects = [RecoverMana(level*5)],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 1
        if isinstance(self.self_effects[0], RecoverMana):
            self.self_effects[0].mana_gain += 5



# -------------------- For Enemy (player should never be able to unlock) ---------
@register_action
class EBite(Action):

    def __init__(self, level: int) -> None:
        super().__init__(
            name = "Bite",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(1 + level, 1, Attack_Type.SHARP, 1)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )
    
    
    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 1

@register_action
class ESling(Action):

    def __init__(self, level: int) -> None:
        super().__init__(
            name = "Slingshot",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(3 + level, 1, Attack_Type.BLUDGEON, 1)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )
    
    
    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 1

@register_action
class EBone(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Bone", 
            level = level, 
            action_type = Action_Type.WEAPON, 
            attacks = [Attack(2 + 3*level, 2, Attack_Type.BLUDGEON, 1)], 
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 3

@register_action
class EDagger(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Dagger",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(3 + level, 1, Attack_Type.SHARP, 2)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 1

@register_action
class EScimitar(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Scimitar",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(3 + 2*level, 1, Attack_Type.SHARP, 2)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 2

@register_action
class EShortbow(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Shortbow",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(3 + 2*level, 1, Attack_Type.SHARP, 1)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 2

@register_action
class ELongbow(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Longbow",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(3 + 3*level, 1, Attack_Type.SHARP, 1)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 3

@register_action
class EMorningstar(Action):
    
    def __init__(self, level: int):
        super().__init__(
            name = "Morningstar",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(8 + 3*level, 1, Attack_Type.SHARP, 1)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 3

@register_action
class EClub(Action):
     
    def __init__(self, level: int):
        super().__init__(
            name = "Club",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(4 + 2*level, 1, Attack_Type.BLUDGEON, 1)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 2

@register_action
class EJavelin(Action):
    
    def __init__(self, level: int):
        super().__init__(
            name = "Javelin",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(2 + 2*level, 1, Attack_Type.SHARP, 1)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 2

@register_action
class EClaws(Action):
    
    def __init__(self, level: int):
        super().__init__(
            name = "Claws",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(2 + level, 1, Attack_Type.SHARP, 2)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 1

@register_action
class ELongsword(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Longsword",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(3 + 3*level, 1, Attack_Type.SHARP, 2)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 3

@register_action
class ESlam(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Slam",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(1 + 2*level, 1, Attack_Type.BLUDGEON, 1)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 2

@register_action
class EFireTouch(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Touch",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(1 + 2*level, 1, Attack_Type.FIRE, 1)],
            target_effects = [DOT("Burn", level, Attack(level, 1, Attack_Type.FIRE, 1))], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 2
        if isinstance(self.target_effects[0], DOT):
            self.target_effects[0].turns_left += 1
            self.target_effects[0].damage.dmg += 1

@register_action
class EHorns(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Horns",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(1 + 2*level, 1, Attack_Type.SHARP, 1)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 2

@register_action
class ETentacles(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Tentacles",
            level = level,
            action_type = Action_Type.WEAPON,
            attacks = [Attack(1 + 2*level, 1, Attack_Type.SHARP, 1)],
            target_effects = [], 
            self_effects = [],
            mana_cost = 0,
            max_level = -1,
            upgrades = []
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 2