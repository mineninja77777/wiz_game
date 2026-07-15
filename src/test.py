# testing entity

from instances.entities import *
from instances.classes import *
from instances.weapons import *
from instances.spells import *
from instances.others import *
from engine.registries import *
from engine.UI import UIManager
from engine.entity import Player

from engine.events import Event

player = Player.create_player()
for i in range(8):
    player.actions[0].level_up()
player.level_up()