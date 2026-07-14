# testing entity

from instances.entities import *
from instances.classes import *
from instances.weapons import *
from instances.spells import *
from instances.others import *
from engine.registries import *
from engine.UI import UIManager

from engine.events import Event


ui_manager: UIManager = UIManager.instance()
ui_manager.print_event(Event('take_damage', name='Bob', dmg=3.4))
ui_manager.print_event(Event('output_stats', name='Bob', hp=4.5, mana=1.2))