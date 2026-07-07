from __future__ import annotations # woah time travel

import math
import random

from engine.base import *
from engine.action import enough_mana, Action, Effect, Attack

from instances.effects import *
from instances.weapons import *
from instances.spells import *
from instances.others import *


from engine.encounter_manager import EncounterManager, register_enemy

from engine.entity import Entity, Enemy


# ---------------------   NPCS? ----------------------------


# ----------------- Player summonables ---------------------
class Summoned_Zombie(Entity):
    def __init__(self, level: int, alignment: bool):
        super().__init__(
            "Zombie the Calm Sea",
            level, 
            alignment, 
            StatBlock(level*5 + 1,0, 0, 1, Attack_Type.generate_resistances()), 
            [EBite(level)]
        )
    
    def level_up(self):
        self.level += 1

        self.stats.max_hp += 5
        for action in self.actions:
            action.level_up()

class Summoned_Skelly(Entity):
    def __init__(self, level: int, alignment: bool):
        super().__init__(
            "Skelly the smelly", 
            level, 
            alignment, 
            StatBlock(level*5,0, 0, 1, Attack_Type.generate_resistances()), 
            [EBite(level), EBone(level)]
        )
    
    def level_up(self):
        self.level += 1

        self.stats.max_hp += 5
        for action in self.actions:
            action.level_up()




# --------------------- Enemies ----------------------------

@register_enemy()
class Rat(Enemy):

    def __init__(self):
        super().__init__(
            "Rat", 
            1, # really ought to be less
            StatBlock(1, 0, 0, 1, Attack_Type.generate_resistances()), 
            [EBite(1)]
        )

@register_enemy()
class Kobold(Enemy):

    def __init__(self):
        super().__init__(
            "Kobold", 
            1,
            StatBlock(5, 0, 0, 1, Attack_Type.generate_resistances()), 
            [EDagger(1), ESling(1)]
        )

@register_enemy()
class Goblin(Enemy):

    def __init__(self):
        super().__init__(
            "Goblin", 
            2,
            StatBlock(7, 0, 0, 1, Attack_Type.generate_resistances()), 
            [EScimitar(1), EShortbow(1)]
        )

@register_enemy()
class Bugbear(Enemy):

    def __init__(self):
        super().__init__(
            "Bugbear", 
            5,
            StatBlock(27, 0, 0, 1, Attack_Type.generate_resistances()), 
            [EMorningstar(1), EJavelin(5)]
        )

@register_enemy()
class Dryad(Enemy):
    
    def __init__(self):
        super().__init__(
            "Dryad", 
            5,
            StatBlock(22, 0.1, 15, 1, Attack_Type.generate_resistances({Attack_Type.MAGICAL: 0.5})), 
            [EClub(0), EEntangle(5)]
        )

@register_enemy()
class Ogre(Enemy):
    
    def __init__(self):
        super().__init__(
            "Ogre", 
            10,
            StatBlock(60, 0, 0, 1, Attack_Type.generate_resistances()), 
            [EClub(5), EJavelin(5)]
        )

@register_enemy()
class Owlbear(Enemy):
    
    def __init__(self):
        super().__init__(
            "Owlbear", 
            15,
            StatBlock(60, 0, 0, 2, Attack_Type.generate_resistances()), 
            [EBite(10), EClaws(10)]
        )

@register_enemy()
class Wolf(Enemy):
    
    def __init__(self):
        super().__init__(
            "Wolf", 
            15,
            StatBlock(60, 0, 0, 2, Attack_Type.generate_resistances({Attack_Type.BLUDGEON: 0.5, Attack_Type.SHARP: 0.5, Attack_Type.FIRE: 2})), 
            [EBite(5), EClaws(5)]
        )

@register_enemy()
class Wight(Enemy):
    
    def __init__(self):
        super().__init__(
            "Wight", 
            15,
            StatBlock(45, 0, 0, 2, Attack_Type.generate_resistances({Attack_Type.NECROTIC: 0.5, Attack_Type.BLUDGEON: 0.5, Attack_Type.SHARP: 0.5})), 
            [ELongsword(1), ELongbow(1), ELifeDrain(1)]
        )

@register_enemy()
class AirElemental(Enemy):

    def __init__(self):
        super().__init__(
            "Air Elemental", 
            25,
            StatBlock(90, 0.5, 30, 2, Attack_Type.generate_resistances({Attack_Type.POISON: 0, Attack_Type.BLUDGEON: 0.5, Attack_Type.SHARP: 0.5})), 
            [ESlam(5), EWhirlwind(5)]
        )

@register_enemy()
class EarthElemental(Enemy):

    def __init__(self):
        super().__init__(
            "Earth Elemental", 
            25,
            StatBlock(130, 0, 0, 2, Attack_Type.generate_resistances({Attack_Type.POISON: 0, Attack_Type.BLUDGEON: 0.5, Attack_Type.SHARP: 0.5})), 
            [ESlam(5)]
        )

@register_enemy()
class FireElemental(Enemy):

    def __init__(self):
        super().__init__(
            "Fire Elemental", 
            25,
            StatBlock(102, 0, 0, 2, Attack_Type.generate_resistances({Attack_Type.POISON: 0, Attack_Type.BLUDGEON: 0.5, Attack_Type.SHARP: 0.5, Attack_Type.WATER: 2})), 
            [EFireTouch(10)]
        )

@register_enemy()
class WaterElemental(Enemy):
    
    def __init__(self):
        super().__init__(
            "Water Elemental", 
            25,
            StatBlock(100, 0, 30, 2, Attack_Type.generate_resistances({Attack_Type.POISON: 0, Attack_Type.BLUDGEON: 0.5, Attack_Type.SHARP: 0.5})), 
            [ESlam(5), EWave(5)]
        )

@register_enemy()
class Wraith(Enemy):
    
    def __init__(self):
        super().__init__(
            "Water Elemental", 
            25,
            StatBlock(100, 0, 50, 2, Attack_Type.generate_resistances({Attack_Type.POISON: 0, Attack_Type.NECROTIC: 0, Attack_Type.BLUDGEON: 0.5, Attack_Type.SHARP: 0.5})), 
            [ELifeDrain(10), Summon(Summoned_Skelly(1, False))]
        )

@register_enemy()
class Chimera(Enemy):
    
    def __init__(self):
        super().__init__(
            "Chimera", 
            30,
            StatBlock(115, 0, 30, 3, Attack_Type.generate_resistances()), 
            [EBite(5), EClaws(5), EHorns(5), EFireBreath(5)]
        )

@register_enemy()
class Cyclops(Enemy):

    def __init__(self):
        super().__init__(
            "Cyclops", 
            30,
            StatBlock(140, 0, 0, 2, Attack_Type.generate_resistances()), 
            [EClub(15), ESlam(15)]
        )

@register_enemy()
class Mage(Enemy):

    def __init__(self):
        super().__init__(
            "Mage", 
            30,
            StatBlock(40, 0, 100, 2, Attack_Type.generate_resistances()), 
            [EssenceStaff(10), HealSelf(5), Firebolt(5), MagicMissiles(5)] # also has fireball but idk if I should add that
        )

    def get_action(self) -> tuple[Action, list[Entity], list[Entity]] | None:
        if self.hp <= 20: # try find a helpful spell
            for action in self.actions:
                if isinstance(action, HealSelf) and self.mana >= action.mana_cost:
                    return action, [], []

        if self.mana <= 20:
            for action in self.actions:
                if isinstance(action, EssenceStaff) and self.mana >= action.mana_cost:
                    return action, \
                           [random.choice(EncounterManager.instance().get_aligned(not self.aligned))], \
                           EncounterManager.instance().get_aligned(not self.aligned)

        return super().get_action()

@register_enemy()
class MindFlayer(Enemy):

    def __init__(self):
        super().__init__(
            "Mind Flayer", 
            35,
            StatBlock(90, 0, 30, 2, Attack_Type.generate_resistances()), 
            [ETentacles(5), EMindBlast(10)] # may want to add more
        )

