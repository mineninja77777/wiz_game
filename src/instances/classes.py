from __future__ import annotations


from engine.base import *
from engine.action import enough_mana, Action, Effect, Attack
from engine.base import StatBlock
from engine.encounter_manager import EncounterManager as em
from engine.entity import Entity, Player
from engine.registries import action_registry, register_class
from engine.events import Event
from engine.UI import UIManager

from instances.weapons import *
from instances.spells import *
from instances.others import *

@register_class
class Warrior(Player):
    class_name = "Warrior"

    def __init__(self, name: str):
        ui_manager: UIManager = UIManager.instance()

        inital_stats: StatBlock = StatBlock(
            max_hp=12,
            dodge=0,
            max_mana=0,
            turns=1,
            resistances=Attack_Type.generate_resistances()
        )

        action_choices: list[Action] = [
            Sword(1),
            Axe(1),
            Mace(1)
        ]
        chosen_actions: list[Action] = [Rest(1)]
        
        for _ in range(2):
            choices: dict[str, Action] = UIManager.generate_options(action_choices)
            chosen_one: Action = ui_manager.get_input(Event('select_actions', actions=list(choices.keys())), choices)
            action_choices.remove(chosen_one)
            chosen_actions.append(chosen_one)

        super().__init__(name, inital_stats, chosen_actions)
    
    def level_up(self):
        self.level += 1

        self.stats.max_hp += 12

        self.upgrade_actions(2)
        
        # special per-level stuff
        if self.level == 2:
            self.stats.dodge += 0.2
        elif self.level == 5:
            self.stats.turns += 1

@register_class
class Mage(Player):
    class_name = "Mage"

    def __init__(self, name: str):
        ui_manager: UIManager = UIManager.instance()

        inital_stats: StatBlock = StatBlock(
            max_hp=6,
            dodge=0,
            max_mana=20,
            turns=1,
            resistances=Attack_Type.generate_resistances({Attack_Type.MAGICAL: 0.5})
        )

        
        action_choices: list[Action] = [
            Firebolt(1),
            MagicMissiles(1),
        ]
        chosen_actions: list[Action] = [
            Staff(1),
            Rest(1)
        ]

        for _ in range(2):
            choices: dict[str, Action] = UIManager.generate_options(action_choices)
            chosen_one: Action = ui_manager.get_input(Event('select_actions', actions=list(choices.keys())), choices)
            action_choices.remove(chosen_one)
            chosen_actions.append(chosen_one)

        super().__init__(name, inital_stats, chosen_actions)
    
    def level_up(self):
        self.level += 1

        self.stats.max_hp += 6

        # add new actions
        # need to work out registries first

        # upgrade some actions
        self.upgrade_actions(3)
        
        # special per-level stuff
        if self.level == 10:
            self.stats.turns += 1