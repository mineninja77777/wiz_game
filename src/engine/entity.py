from __future__ import annotations # woah time travel
from typing import TYPE_CHECKING

from time import sleep
import random
from engine.base import *
from engine.action import enough_mana, Action, Effect, Attack

from engine.encounter_manager import EncounterManager

class Entity:
    name: str
    aligned: bool # player is aligned, enemies are not (aka good/evil)

    level: int # doesn't affect stats, is only tracking how many times has been levelled

    hp: float
    mana: float
    stats: StatBlock

    actions: list[Action]

    active_effects: list[Effect]

    def __init__(self, name: str, level: int, aligned: bool, stats: StatBlock, actions: list[Action]):
        self.name = name
        self.aligned = aligned
        self.level = level
        self.stats = stats

        self.hp = stats.max_hp
        self.mana = stats.max_mana

        self.actions = actions

        self.active_effects = []

    def turn(self):
        blocked = False
        for effect in self.active_effects:
            if effect.blocks_turn(self):
                blocked = True

        if not blocked:
            for _ in range(self.stats.turns):
                action = self.get_action()
                if action:
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
        
        if action.attacks[0].dmg > 0:
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
            if primary_targets[i].stats.dodge > random.random():
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

    def recieve_effect(self, effect: Effect):
        self.active_effects.append(effect)
        effect.on_apply(self)

    def tick_effects(self):
        for effect in self.active_effects.copy():
            if effect.expired(self):
                effect.remove(self)
            else:
                effect.tick(self)
    
    def level_up(self):
        pass


class Enemy(Entity):
    def __init__(self, name: str, level: int, stats: StatBlock, actions: list[Action]):
        super().__init__(name, level, False, stats, actions)
    