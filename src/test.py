# testing entity

import inspect

import engine.action
import engine.base
import engine.entity
import engine.encounter_manager
import engine.game_manager
import instances.effects
import instances.entities
import instances.others
import instances.spells
import instances.weapons

# stats = StatBlock(100,0,50,1,{})
# for attack_type in Attack_Type:
#     stats.resistances[attack_type] = 1

# entity1 = Entity("1", 1, True, stats, [])
# entity2 = Entity("2", 1, False, stats, [])

# entity1.execute_action(spells.Rot(1), [entity2], [entity2])

# while not len(entity2.active_effects) == 0:
#     entity2.tick_effects()
#     print(entity2.hp)

# entity2.execute_action(others.Rest(1), [], [])
# while not len(entity2.active_effects) == 0:
#     entity2.tick_effects()
#     print(entity2.hp)

# print(inspect.getmembers(instances.entities))