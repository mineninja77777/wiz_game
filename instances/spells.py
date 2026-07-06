from __future__ import annotations # woah time travel
from typing import TYPE_CHECKING

from base import Action_Type, Attack_Type
from action import Action, Attack, Effect
from instances.effects import *

if TYPE_CHECKING:
    from entity import Entity


class Firebolt(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Firebolt",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [Attack(5 + 3*level, 2, Attack_Type.FIRE, 1)],
            target_effects = [],
            self_effects = [],
            mana_cost = 5,
            max_level = 20,
            upgrades = [Firebolt, Fireball] # can remain a firebolt as fireball may be too costly mana-wise
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 3

class Fireball(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Fireball",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [Attack(5 + 10*level, 2, Attack_Type.FIRE, 100)],
            target_effects = [],
            self_effects = [],
            mana_cost = 50,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 10


class MagicMissiles(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Magic Missiles",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [
                Attack(1 + level * 0.5, 1, Attack_Type.SHARP, 1), 
                Attack(1 + level * 0.5, 1, Attack_Type.SHARP, 1),
                Attack(1 + level * 0.5, 1, Attack_Type.SHARP, 1)
            ],
            target_effects = [],
            self_effects = [],
            mana_cost = 4,
            max_level = 10,
            upgrades = [MissileStorm] 
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 0.5
        self.attacks[1].dmg += 0.5
        self.attacks[2].dmg += 0.5

class MissileStorm(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Missile Storm",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [
                Attack(1 + level, 1, Attack_Type.SHARP, 10), 
                Attack(1 + level, 1, Attack_Type.SHARP, 10),
                Attack(1 + level, 1, Attack_Type.SHARP, 10)
            ],
            target_effects = [],
            self_effects = [],
            mana_cost = 15,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 1
        self.attacks[1].dmg += 1
        self.attacks[2].dmg += 1


class EtherealStrike(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Ethereal Strike",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [Attack(6 + 4*level, 1, Attack_Type.MAGICAL, 1)],
            target_effects = [],
            self_effects = [],
            mana_cost = 8,
            max_level = 25,
            upgrades = [PWK] 
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 4

class PWK(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Power Word Kill",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [Attack(500 + 10*level, 0, Attack_Type.MAGICAL, 1)],
            target_effects = [],
            self_effects = [],
            mana_cost = 8,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 10


class Rot(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Rot",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [Attack(0, 0, Attack_Type.VOID, 1)],
            target_effects = [DOT("Rot", 3, Attack(2*level, 1, Attack_Type.MAGICAL, 1))],
            self_effects = [],
            mana_cost = 4,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        if isinstance(self.target_effects[0], DOT):
            self.target_effects[0].damage.dmg += 2


class Hold(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Hold Person",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [Attack(0, 0, Attack_Type.VOID, 1)],
            target_effects = [Stun(2 + level)],
            self_effects = [],
            mana_cost = 8,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        if isinstance(self.target_effects[0], Stun):
            self.target_effects[0].turns_left += 1


class Good(Action): # should probably be player-only, as player should be immune at least

    def __init__(self, level: int):
        super().__init__(
            name = "Friends",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [Attack(0, 0, Attack_Type.VOID, 1)],
            target_effects = [Realign(True, level)],
            self_effects = [],
            mana_cost = 15,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        if isinstance(self.target_effects[0], Realign):
            self.target_effects[0].level += 1

class Summon(Action):

    # summonee's level is the spell's
    def __init__(self, summonee: Entity):
        super().__init__(
            name = "Summon Undead",
            level = summonee.level,
            action_type = Action_Type.SPELL,
            attacks = [],
            target_effects = [],
            self_effects = [SummonEffect(summonee)],
            mana_cost = 20,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        if isinstance(self.self_effects[0], SummonEffect):
            self.self_effects[0].summonee.level_up()

class HealSelf(Action): # should probably be player-only, as player should be immune at least

    def __init__(self, level: int):
        super().__init__(
            name = "Heal",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [],
            target_effects = [],
            self_effects = [Heal(level*0.1, percent = True)],
            mana_cost = 10,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        if isinstance(self.self_effects[0], Heal):
            self.self_effects[0].heal += 0.1

# ------------------------ Enemy Spells ------------------------------

class EEntangle(Action):
    
    def __init__(self, level: int):
        super().__init__(
            name = "Entangle",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [Attack(level, 1, Attack_Type.BLUDGEON, 1)],
            target_effects = [Stun(1)],
            self_effects = [],
            mana_cost = 5,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 1

class ELifeDrain(Action):
    
    def __init__(self, level: int):
        super().__init__(
            name = "Life Drain",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [Attack(3 + 2*level, 1, Attack_Type.NECROTIC, 1)],
            target_effects = [HPMaxReduction(3 + 2*level)],
            self_effects = [],
            mana_cost = 5,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 2

class EWhirlwind(Action):
    
    def __init__(self, level: int):
        super().__init__(
            name = "Whirlwind",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [Attack(3 + 2*level, 1, Attack_Type.BLUDGEON, 10)],
            target_effects = [Prone()],
            self_effects = [],
            mana_cost = 10,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 2

class EWave(Action):
    
    def __init__(self, level: int):
        super().__init__(
            name = "Wave",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [Attack(3 + 2*level, 1, Attack_Type.BLUDGEON, 10)],
            target_effects = [Prone(), DOT("Drowning", 3, Attack(level*2, 1, Attack_Type.WATER, 1))],
            self_effects = [],
            mana_cost = 10,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 2
        if isinstance(self.target_effects[1], DOT):
            self.target_effects[1].turns_left += 1
            self.target_effects[1].damage.dmg += 2

class EFireBreath(Action):
    
    def __init__(self, level: int):
        super().__init__(
            name = "Fire Breath",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [Attack(5 + 5*level, 2, Attack_Type.FIRE, 10)],
            target_effects = [],
            self_effects = [],
            mana_cost = 5,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 5

class EMindBlast(Action):

    def __init__(self, level: int):
        super().__init__(
            name = "Mind Blast",
            level = level,
            action_type = Action_Type.SPELL,
            attacks = [Attack(5 + 5*level, 2, Attack_Type.PSYCHIC, 10)],
            target_effects = [Stun(5)],
            self_effects = [],
            mana_cost = 30,
            max_level = -1,
            upgrades = [] 
        )

    def level_up(self):
        self.level += 1
        self.attacks[0].dmg += 5