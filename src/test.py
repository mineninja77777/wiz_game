# testing entity

import instances.entities
import engine.encounter_manager as em

print(em._enemy_registry)

tst: em.Encounter = em.Encounter(3)
print(tst.encounter_contents)