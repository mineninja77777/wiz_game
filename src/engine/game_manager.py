from __future__ import annotations # woah time travel
from typing import cast
import random

from engine.base import Action_Type, Attack_Type
from engine.action import Action, Attack, Effect
from engine.entity import Entity, Player
from engine.encounter_manager import EncounterManager as em
from engine.events import Event
from engine.UI import UIManager

class GameManager:
    _instance: GameManager | None = None

    players: list[Player]
    difficulty: int # the difficulty

    def __init__(self):
        self.players = []
        
        self.players.append(Player.create_player())
        self.difficulty = int(input("Difficulty: (1/2/3)")) # placeholder

        self.main()

    def main(self):
        

        result: bool = em.instance().run_encounter(sum(player.level for player in self.players) * self.difficulty // 2 + 1, cast(list[Entity], self.players))
        
        if not result:
            UIManager.print_event(Event('lose'))
            return
        UIManager.print_event(Event('win_encounter'))
        self.remove_dead()

        level_up: bool = random.choice([True, False])
        for player in self.players:
            if level_up:
                player.level_up()
                player.rest()
            else:
                player.rest(False)

        self.main()


    def remove_dead(self):
        i = 0
        while i < len(self.players):
            if self.players[i].hp <= 0:
                self.players.remove(self.players[i])
            i += 1

    @classmethod
    def instance(cls) -> GameManager:
        if cls._instance is None:
            cls._instance = GameManager()
        return cls._instance