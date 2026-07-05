from dataclasses import dataclass
from enum import Enum
from typing import cast
import random
import math
from time import sleep

"""
NOTE:
Some typecasting stuff is in this code because I'm using vscode type checking; no idea if IDLE supports it

TODO:
Code can be much improved
Gameplay loop can be added, allowing player to face multiple ecounters
Dialogue revamp
"""


class Attack_Type(Enum):
    """ different types of attacks """
    VOID = 0
    SHARP = 1
    BLUDGEON = 2
    MAGICAL = 3
    FIRE = 4


@dataclass
class Damage:
    """ helps determine how much damage an attack does with spread """
    dmg: float
    spread: float
    dmg_type: Attack_Type

    def getDamage(self) -> float:
        return round(random.normalvariate(self.dmg, self.spread/3)) # spread is 3σ so that dmg is almost always dmg ± spread


@dataclass
class Action:
    name: str
    dmg: Damage
    heal: float
    aoe: int
    mana_cost: float # negative values can be used to gain mana

class Entity:
    def __init__(self, name: str, level: int, alignment: int, max_hp: float, actions: list[Action], max_mana: float, turns: int, resistances: dict[Attack_Type, float]):
        """ resistances is dict with atk type to dmg multiplier """

        self.name = name
        self.level = level
        self.alignment = alignment
        self.max_hp = max_hp
        self.hp = max_hp
        self.actions = actions
        self.max_mana = max_mana
        self.mana = max_mana
        self.turns = turns
        self.resistances = resistances
    
    def take_dmg(self, dmg: Damage) -> tuple[float, bool]:
        damage_taken = dmg.getDamage() * self.resistances[dmg.dmg_type]
        self.hp -= damage_taken
        return damage_taken, self.hp <= 0


class Enemy(Entity):
    def __init__(self, name: str, level: int, max_hp: float, actions: list[Action], max_mana: float, turns: int, resistances: dict[Attack_Type, float], alignment: int = -1):
        """ resistances is dict with atk type to dmg multiplier """
        super().__init__(name, level, alignment, max_hp, actions, max_mana, turns, resistances)


    def get_action(self, targets: list[Entity]) -> tuple[Action, Entity]: # should only return None if no actions can be performed
        """ evaluates which action to take based on mana and hp """
        scores = []

        target = targets[0]
        for entity in targets:
            if entity.alignment > target.alignment:
                target = entity # target good people
            elif entity.mana > target.mana:
                target = entity # target magic people
            elif entity.hp > target.hp:
                target = entity 

        for action in self.actions:
            if action.mana_cost > self.mana:
                scores.append(0)
                continue


            score = 0

            # score based on damage
            score += (action.dmg.dmg - action.dmg.spread) * target.resistances[action.dmg.dmg_type] / target.hp # use attack's min damage

            # score from heal
            score += action.heal / self.hp

            # score from mana cost
            if self.mana != 0:
                score -= action.mana_cost / self.mana

            scores.append(score)

        return random.choices(self.actions, scores, k=1)[0], target

    # some default enemies
    @staticmethod
    def Rat(level: int) -> 'Enemy':
        hp = 3 + level * 2
        actions = [
            Action("Bite", Damage(2 + level, 1, Attack_Type.SHARP), 0, 1, 0)
        ]
        return Enemy(f"Rat", level, 3 + level * 2, actions, 0, 1, {atk_type: 1.0 for atk_type in Attack_Type})

    @staticmethod
    def Goblin(level: int) -> 'Enemy':
        hp = 5 + level * 3
        actions = [
            Action("Stab", Damage(3 + level, 1, Attack_Type.SHARP), 0, 1, 0),
            Action("Bonk", Damage(4 + level, 2, Attack_Type.BLUDGEON), 0, 1, 0)
        ]
        return Enemy(f"Goblin", level, hp, actions, 0, 1, {atk_type: 1.0 for atk_type in Attack_Type})

    @staticmethod
    def Dark_Mage(level: int) -> 'Enemy':
        hp = 15 + level * 2
        actions = [
            Action("Firebolt", Damage(6 + level, 2, Attack_Type.FIRE), 0, 1, 3),
            Action("Magic Missile", Damage(4 + level, 1, Attack_Type.MAGICAL), 0, 1, 2),
            Action("Heal", Damage(0, 0, Attack_Type.VOID), 5 + level, 0, 3)
        ]
        resistances = {atk_type: 1.0 for atk_type in Attack_Type}
        resistances[Attack_Type.MAGICAL] = 0.5 # Dark Mages have magical barriers
        resistances[Attack_Type.FIRE] = 1.5 # Dark Mages' robes are flammable 
        return Enemy(f"Dark Mage", level, hp, actions, 10 + level * 5, 1, resistances)

class Player(Entity):
    def __init__(self, name: str, max_hp: float, actions: list[Action], turns: int, max_mana: float):
        alignment = 1
        super().__init__(name, 1, alignment, max_hp, actions, max_mana, turns, {atk_type: 1.0 for atk_type in Attack_Type})
    
    def get_action(self, targets: list[Entity]) -> tuple[Action, list[Entity]]:
        action_names: list[str] = [action.name.lower() for action in self.actions]

        print("Which action doest thou wish to take of the following?")
        print(" - " + "\n - ".join(action_names))
        choice = input().lower()
        while (choice not in action_names) or self.actions[action_names.index(choice)].mana_cost > self.mana:
            print(f"My sincerest apologies, {self.name}, but I fail to comprehend thy words.")
            print("Which action doest thou wish to take?")
            choice = input().lower()
        
        final = self.actions[action_names.index(choice)]

        if final.aoe == 1:
            print("Who wouldst thou like to target? (input the number)")
            for i in range(len(targets)):
                print(f"{i}: A {targets[i].name} of proficiency {targets[i].level}")
            target = input()
            while not (target.isnumeric() and 0 <= int(target) < len(targets)):
                print(f"My sincerest apologies, {self.name}, but I fail to comprehend thy words.")
                print("Who wouldst thou like to target? (input the number)")
                target = input()
            return final, [targets[int(target)]]

        return final, targets[:final.aoe]



class Game_Manager:
    def __init__(self):
        # set up player
        self.setup_player()
        print(f"{self.player.name}, I must first ask of thee to tell me of thy bravery. How strong is thy heart? (Difficulty: Easy | Medium | Hard)")
        difficulty = input().lower()
        while difficulty not in ["easy", "medium", "hard"]:
            print(f"""My sincerest apologies, {self.player.name}, but I fail to comprehend thy words. 
                Pray, inform me of thy bravery. How strong is thy heart? (Difficulty: Easy | Medium | Hard)""")
            difficulty = input().lower()
        
        if difficulty == "easy":
            print(f"Fear not, {self.player.name}, I shall avoid placing thee in peril. Thou shalt face foes of lesser strength.")
            self.difficulty = 1
        elif difficulty == "medium":
            print(f"I see thou art brave, {self.player.name}. Thou shalt face foes of moderate strength.")
            self.difficulty = 2
        elif difficulty == "hard":
            print(f"Brave soul! I sense great courage within thee, {self.player.name}. Thou shalt face the most formidable foes.")
            self.difficulty = 3
        sleep(0.5)
        # set up enemies
        self.enemies: list[Enemy] = []

        if self.difficulty == 1:
            self.enemies.append(Enemy.Rat(1))
            self.enemies.append(Enemy.Rat(1))
        elif self.difficulty == 2:
            self.enemies.append(Enemy.Goblin(1))
            self.enemies.append(Enemy.Rat(1))
        elif self.difficulty == 3:
            self.enemies.append(Enemy.Rat(1))
            self.enemies.append(Enemy.Rat(2))
            self.enemies.append(Enemy.Goblin(2))
        
        print("Thy adventure may now commence, adventurer. May the fates be with thee.")
        sleep(1)
        self.main()
        
        
    def setup_player(self):

        print("Good day, dearest adventurer. What shalt thou call thyself?")
        name = input()
        print(f"Welcome, {name}. Thou art a brave soul indeed.")
        sleep(0.5)
        print("Which path, then, shalt thy footsteps tread? Warrior or Mage?")
        character_class = input().lower()
        while character_class not in ["warrior", "mage"]:
            print(f"My sincerest apologies, {name}, but I fail to comprehend thy words. Pray, inform me of thy being: Warrior or Mage?")
            character_class = input().lower()
        if character_class == "warrior":
            actions = [
                Action("Slash", Damage(3, 1, Attack_Type.SHARP), 0, 3, 0),
                Action("Smash", Damage(5, 2, Attack_Type.BLUDGEON), 0, 1, 0),
                Action("Heal", Damage(0, 0, Attack_Type.VOID), 15, 0, 3),
                Action("Rest", Damage(0, 0, Attack_Type.VOID), 5, 0, -3)
            ]
            max_hp = 30
            max_mana = 3
        elif character_class == "mage":
            actions = [
                Action("Firebolt", Damage(6, 1, Attack_Type.FIRE), 0, 1, 2),
                Action("Magic Missiles", Damage(4, 1, Attack_Type.MAGICAL), 0, 3, 3),
                Action("Heal", Damage(0, 0, Attack_Type.VOID), 10, 0, 3),
                Action("Rest", Damage(0, 0, Attack_Type.VOID), 3, 0, -5)
            ]
            max_hp = 15
            max_mana = 15
        else:
            raise Exception("no bueno")

        self.player = Player(name, max_hp, actions, 1, max_mana)

        print(f"Why, {name}, I am certain that thou shalt make a valiant {character_class} indeed.")
        sleep(0.5)
        print("Now hence, thou may go forth, and may thy journey be as rich in tale as it is bold in deed!")

        sleep(1)

    def main(self):
        
        initiative: int = 0 # whose go it is: 0 is player, other is self.enemies[initiative - 1]
        while len(self.enemies) > 0:
            sleep(0.5)
            print("")
            if initiative == 0:
                if len(self.enemies) == 1:
                    print("A solitary adversary yet awaits you:")
                else:
                    print(f"Lo, {len(self.enemies)} fell foes do stand across our path:")

                
                for enemy in self.enemies:
                    print(f"A {enemy.name} of proficiency {enemy.level}")
                
                sleep(0.5)
                if self.player.hp == self.player.max_hp:
                    print(f"Thy health doth outshine the noon-day sun. ({math.ceil(self.player.hp)}/{math.ceil(self.player.max_hp)})")
                else:
                    print(f"But {math.ceil(self.player.hp)} of {math.ceil(self.player.max_hp)} candles burn")

                if self.player.mana == self.player.max_mana:
                    print(f"Thy resevoir of arcane might may doth brim o'er. ({math.ceil(self.player.mana)}/{math.ceil(self.player.max_mana)})")
                else:
                    print(f"A mere {math.ceil(self.player.mana)} thimblefuls of essence remain where {math.ceil(self.player.max_mana)} did once.")
                
                sleep(0.5)
                # player's turn
                print("Come forth, bold soul! Thy time is now")
                for _ in range(self.player.turns):
                    action, targets = self.player.get_action(cast(list[Entity], self.enemies))
                    for target in targets:
                        dmg, died = target.take_dmg(action.dmg)
                        print(f"Thou hast dealt {math.ceil(dmg)} damage to the {target.name}.")
                        if died:
                            print(f"As a result of that, {target.name} has perished! Congratulations!")
                    self.player.hp += action.heal
                    self.player.mana -= action.mana_cost

                    if self.player.hp > self.player.max_hp:
                        self.player.hp = self.player.max_hp

                    if self.player.mana > self.player.max_mana:
                        self.player.mana = self.player.max_mana

                    # print some stuff
                    if action.heal != 0: 
                        print(f"You have healed {action.heal} health")
                    if action.mana_cost < 0:
                        print(f"You have recovered {-action.mana_cost} mana")
                    elif action.mana_cost > 0:
                        print(f"You have expended {action.mana_cost} mana")

            else:
                current = self.enemies[initiative-1]
                # enemy turn

                for _ in range(current.turns):
                    result = current.get_action(cast(list[Entity], self.enemies + [self.player]))
                    if not result:
                        raise Exception("could've rested tbh")
                    else:
                        dmg = result[1].take_dmg(result[0].dmg)[0]
                        current.hp += result[0].heal
                        current.mana -= result[0].mana_cost

                        print(f"A {current.name} did a {result[0].name}, and as a result {"you" if result[1].name == self.player.name else result[1].name} took {math.ceil(dmg)} damage")
            for enemy in self.enemies.copy():
                if enemy.hp <= 0:
                    self.enemies.remove(enemy)
            if self.player.hp <= 0:
                print("You have perished.")
                return

            initiative = (initiative + 1) % (len(self.enemies) + 1)

game_manager = Game_Manager()