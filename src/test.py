# testing entity

from instances.entities import *
from engine.action import Attack, Attack_Type
import engine.encounter_manager as em

# print(em._enemy_registry)

encounter_manager = em.EncounterManager.instance()
encounter_manager.run_encounter(5, [Summoned_Skelly(10, True)])