from __future__ import annotations
from collections.abc import Callable

from dataclasses import dataclass
from enum import Enum
"""
NOTE:
Some typecasting stuff is in this code because I'm using vscode type checking; no idea if IDLE supports it

TODO:
Code can be much improved
Gameplay loop can be added, allowing player to face multiple ecounters
"""

class Attack_Type(Enum):
    """ different types of attacks """
    VOID = 0
    SHARP = 1
    BLUDGEON = 2
    MAGICAL = 3
    FIRE = 4
    WATER = 5
    COLD = 6
    NECROTIC = 7
    POISON = 8
    PSYCHIC = 9


    @classmethod
    def generate_resistances(cls, dct: dict[Attack_Type, float] = {}) -> dict[Attack_Type, float]:
        final: dict[Attack_Type, float] = {}
        for typ in Attack_Type:
            if typ in list(dct.keys()):
                final[typ] = dct[typ]
            else:
                final[typ] = 1
        return final

class Action_Type(Enum):
    """ different kinds of action innit """
    WEAPON = 0
    SPELL = 1
    OTHER = 2 # generally non-violent


@dataclass
class StatBlock:
    max_hp: float
    dodge: float # dodge chance (0-1)
    max_mana: float
    turns: int # how many turns it gets in battle
    resistances: dict[Attack_Type, float] # resistances / weaknesses


