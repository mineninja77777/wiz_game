from __future__ import annotations # woah time travel
from typing import TYPE_CHECKING

from time import sleep
import random
from engine.base import *
from engine.action import enough_mana, Action, Effect, Attack

from engine.base import StatBlock
from engine.encounter_manager import EncounterManager

from engine.events import Event
from engine.UI import UIManager

from engine.registries import class_registry

class Entity:
    _next_id = 0

    name: str
    uid: int # should be unique

    aligned: bool # player is aligned, enemies are not (aka good/evil)

    level: int # doesn't affect stats, is only tracking how many times has been levelled

    hp: float
    mana: float
    stats: StatBlock

    actions: list[Action]

    active_effects: list[Effect]

    def __init__(self, name: str, level: int, aligned: bool, stats: StatBlock, actions: list[Action]):
        self.name = name
        self.uid = Entity._next_id
        Entity._next_id += 1
        self.aligned = aligned
        self.level = level
        self.stats = stats

        self.hp = stats.max_hp
        self.mana = stats.max_mana

        self.actions = actions

        self.active_effects = []

    def __del__(self):
        if self.uid == Entity._next_id - 1: # try do some cleanup, even if not enough
            Entity._next_id -= 1

    def turn(self):
        UIManager.print_event(Event('enemy_start_turn', name=self.name))
        for _ in range(self.stats.turns):
            if self.is_blocked():
                continue

            action = self.get_action()
            if action:
                UIManager.print_event(Event('takes_action', name=self.name, action_name=action[0].name))
                self.execute_action(*action)
        
        self.tick_effects()

    def get_action(self) -> tuple[Action, list[Entity], list[Entity]] | None:
        # returns action, primary targets, other potential targets
        encounter: EncounterManager = EncounterManager.instance()

        # literally just pick random
        
        useable_actions: list[Action] = enough_mana(self.actions, self.mana)
        if len(useable_actions) == 0: return None
        action = random.choice(useable_actions)

        # filter targets so that bad things happen to enemies (aka aligned differently)
        
        if len(action.attacks) > 0 and action.attacks[0].dmg > 0:
            targets: list[Entity] = encounter.get_aligned(not self.aligned) # target enemies
        else:
            targets: list[Entity] = encounter.get_aligned(self.aligned) # target allies
        
        if len(targets) == 0: return None
        # choose targets
        primary_targets = random.choices(targets, k=len(action.attacks))


        return action, primary_targets, targets

    # worry about returning info later # targets should be all entities of opposite alignment # or same if it is a nice action
    def execute_action(self, action: Action, primary_targets: list[Entity], targets: list[Entity]): #
        if len(action.attacks) != len(primary_targets):
            raise Exception("uhhhhhhhh no bueno innnit blud")
        
        for i in range(len(action.attacks)):
            if primary_targets[i].stats.dodge < random.random():
                # resolve primary target
                primary_targets[i].recieve_attack(action.attacks[i])
                
                # resolve effects on primary target
                for effect in action.target_effects:
                    primary_targets[i].recieve_effect(effect)

            # resolve aoe
            aoe_targets = targets.copy()
            aoe_targets.remove(primary_targets[i]) # don't want to damage primary again
            for target in aoe_targets[:(action.attacks[i].aoe-1)]:
                if target.stats.dodge <= random.random(): continue # dodged

                target.recieve_attack(action.attacks[i])
                
                # handle effects
                for effect in action.target_effects:
                    target.recieve_effect(effect)
            
        for effect in action.self_effects:
            self.recieve_effect(effect)
    
    def recieve_attack(self, attack: Attack): # worry about returning info later
        damage = attack.get_damage() * self.stats.resistances[attack.dmg_type]
        self.hp -= damage
        self.hp = round(self.hp, 1) # because points float
        UIManager.print_event(Event('take_damage', name=self.name, dmg=damage))
        if self.is_dead(): 
            UIManager.print_event(Event('dies', name=self.name))
            EncounterManager.instance().entities.remove(self)

    def recieve_effect(self, effect: Effect):
        UIManager.print_event(Event('recieve_effect', name=self.name, effect=effect.name))
        self.active_effects.append(effect)
        effect.on_apply(self)

    def tick_effects(self):
        for effect in self.active_effects.copy():
            if effect.expired(self):
                effect.remove(self)
            else:
                effect.tick(self)
    
    def clear_effects(self):
        for effect in self.active_effects:
            effect.remove(self)
    
    def rest(self, long: bool = True):
        
        self.clear_effects()

        if long:
            UIManager.print_event(Event('long_rest', name=self.name))
        else:
            UIManager.print_event(Event('short_rest', name=self.name))

        
        self.hp += self.stats.max_hp * (1 - 0.5 * (not long))
        if self.hp > self.stats.max_hp:
            self.hp = self.stats.max_hp
        
        self.mana += self.stats.max_mana * (1 - 0.5 * (not long))
        if self.mana > self.stats.max_mana:
            self.mana = self.stats.max_mana
        
    
    def is_blocked(self) -> bool:
        if self.is_dead(): 
            return True
        blocked = False
        for effect in self.active_effects:
            if effect.blocks_turn(self):
                blocked = True
        return blocked


    def is_dead(self) -> bool:
        return self.hp <= 0
    

class Player(Entity):
    class_name = "NO CLASS"

    def __init__(self, name: str, stats: StatBlock, actions: list[Action]):
        super().__init__(name, 1, True, stats, actions)

    def level_up(self):
        self.level += 1
        UIManager.print_event(Event('level_up', name=self.name, level=self.level))

    def turn(self):
        UIManager.print_event(Event('player_start_turn', name=self.name))
        UIManager.print_event(Event('output_stats', name=self.name, hp=self.hp, mana=self.mana))
        UIManager.print_event(Event('output_effects', name=self.name, effects=[effect.name for effect in self.active_effects]))
        return super().turn()

    def get_action(self) -> tuple[Action, list[Entity], list[Entity]] | None:
        encounter: EncounterManager = EncounterManager.instance()
        
        a_options = UIManager.generate_options(enough_mana(self.actions, self.mana))
        action: Action = UIManager.get_input(Event('select_action', actions=list(a_options.keys())), a_options)

        # filter targets so that bad things happen to enemies (aka aligned differently)
        
        if len(action.attacks) > 0 and action.attacks[0].dmg > 0:
            targets: list[Entity] = encounter.get_aligned(not self.aligned) # target enemies
        else:
            targets: list[Entity] = encounter.get_aligned(self.aligned) # target allies
        
        primary_targets: list[Entity] = []
        for _ in range(len(action.attacks)):
            t_options = UIManager.generate_options(targets, str_func=lambda a: a.name)
            primary_targets.append(UIManager.get_input(Event('select_target', enemies=list(t_options.keys())), t_options))
        
        return action, primary_targets, targets


    def select_new_action(self, actions: list[Action]):

        possibilities: list[Action] = []
        for action in actions:
            if not action in self.actions:
                possibilities.append(action)
        if len(possibilities) == 0: return # all actions are already owned

        options: dict[str, Action] = UIManager.generate_options(possibilities)
        action = UIManager.get_input(Event('gain_new_actions', actions=list(options.keys())), options)

        self.actions.append(action)


    def upgrade_actions(self, number: int):
        
        for _ in range(number):
            options: dict[str, Action] = UIManager.generate_options(self.actions)
            action = UIManager.get_input(Event('level_up_actions', actions=list(options.keys())), options)
            action.level_up()
            if action.max_level != -1 and action.level >= action.max_level:
                upgrade_options = UIManager.generate_options(action.upgrades, lambda upgrade : upgrade(1).name)
                chosen_upgrade = UIManager.get_input(Event('upgrade_action', action_name=action.name, upgrades=list(upgrade_options.keys())), upgrade_options)
                self.actions.remove(action)
                self.actions.append(chosen_upgrade(action.level))

    @staticmethod
    def create_player() -> Player:
        
        name: str = UIManager.get_input(Event('input_name'))
        class_options = {class_.class_name: class_ for class_ in class_registry}
        player_class = UIManager.get_input(Event('select_class', classes=list(class_options.keys())), class_options)
        
        return player_class(name)


class Enemy(Entity):
    def __init__(self, name: str, level: int, stats: StatBlock, actions: list[Action]):
        super().__init__(name, level, False, stats, actions)
    