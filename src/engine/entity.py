from __future__ import annotations # woah time travel
from typing import TYPE_CHECKING

from time import sleep
import random
from engine.base import *
from engine.action import enough_mana, Action, Effect, Attack


if TYPE_CHECKING:
    from engine.context import EncounterContext

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

    def turn(self, context: EncounterContext):
        blocked = False
        for effect in self.active_effects:
            if effect.blocks_turn(self, context):
                blocked = True

        if not blocked:
            for _ in range(self.stats.turns):
                action = self.get_action(context)
                if action:
                    self.execute_action(*action, context)
        
        self.tick_effects(context)

    def get_action(self, context: EncounterContext) -> tuple[Action, list[Entity], list[Entity]] | None:
        # returns action, primary targets, other potential targets

        # literally just pick random
        
        useable_actions: list[Action] = enough_mana(self.actions, self.mana)
        if len(useable_actions) == 0: return None
        action = random.choice(useable_actions)

        # filter targets so that bad things happen to enemies (aka aligned differently)
        
        if action.attacks[0].dmg > 0:
            targets: list[Entity] = context.get_aligned(not self.aligned) # target enemies
        else:
            targets: list[Entity] = context.get_aligned(self.aligned) # target allies
        
        if len(targets) == 0: return None
        # choose targets
        primary_targets = random.choices(targets, k=len(action.attacks))


        return action, primary_targets, targets

    # worry about returning info later # targets should be all entities of opposite alignment # or same if it is a nice action
    def execute_action(self, action: Action, primary_targets: list[Entity], targets: list[Entity], context: EncounterContext): #
        if len(action.attacks) != len(primary_targets):
            raise Exception("uhhhhhhhh no bueno innnit blud")
        
        for i in range(len(action.attacks)):
            if primary_targets[i].stats.dodge > random.random():
                # resolve primary target
                primary_targets[i].recieve_attack(action.attacks[i], context)
                
                # resolve effects on primary target
                for effect in action.target_effects:
                    primary_targets[i].recieve_effect(effect, context)

            # resolve aoe
            aoe_targets = targets.copy()
            aoe_targets.remove(primary_targets[i]) # don't want to damage primary again
            for target in aoe_targets[:(action.attacks[i].aoe-1)]:
                if target.stats.dodge <= random.random(): continue # dodged

                target.recieve_attack(action.attacks[i], context)
                
                # handle effects
                for effect in action.target_effects:
                    target.recieve_effect(effect, context)
            
            
        
        for effect in action.self_effects:
            self.recieve_effect(effect, context)
    
    # enemies should only ever be damaged like this
    def recieve_attack(self, attack: Attack, context: EncounterContext): # worry about returning info later
        damage = attack.get_damage() * self.stats.resistances[attack.dmg_type]
        self.hp -= damage
        self.hp = round(self.hp, 1) # because points float
        if self.hp <= 0:
            context.remove_entity(self)

    def recieve_effect(self, effect: Effect, context: EncounterContext):
        self.active_effects.append(effect)
        effect.on_apply(self, context)

    def tick_effects(self, context: EncounterContext):
        for effect in self.active_effects.copy():
            if effect.expired(self, context):
                effect.remove(self, context)
            else:
                effect.tick(self, context)
    
    def level_up(self):
        pass


class Enemy(Entity):
    def __init__(self, name: str, level: int, stats: StatBlock, actions: list[Action]):
        super().__init__(name, level, False, stats, actions)
    