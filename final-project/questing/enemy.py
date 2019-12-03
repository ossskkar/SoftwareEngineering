from math import ceil
from typing import List

import numpy as np

from .unit import Unit
from .attack import MagicAttack, MeleeAttack, RangedAttack
from .defense import ArmoredDefense, Barrier, Defense
from .types import Position


class Enemy(Unit):
    """Base class for enemy units"""
    def __init__(self, level: int, **kwargs):
        super().__init__(**kwargs)
        self.level = level

    def __str__(self) -> str:
        return f"{self.short_text}({self.level})"

    @staticmethod
    def random_enemy(level: int) -> "Enemy":
        """Creates a random enemy of the specified level."""
        enemy_classes = [Archer, Swordsman, Apprentice]

        enemy_class = np.random.choice(enemy_classes)

        return enemy_class.create(level=level)


class Archer(RangedAttack, Defense, Enemy):
    """Archers are a type of enemy that have ranged attack"""
    NUM_UNITS = 0
    BASE_HEALTH = 3
    BASE_RANGE = 2
    BASE_POWER = 3
    BASE_SPEED = 1

    @classmethod
    def create(cls, level: int) -> "Archer":
        """Creates a new Archer instance of the specified level."""
        health = cls.BASE_HEALTH * level
        attack_range = ceil(cls.BASE_RANGE + level * .2)
        power = cls.BASE_POWER + level
        speed = ceil(cls.BASE_SPEED + level * .1)
        cls.NUM_UNITS += 1
        name = f"{cls.__name__} {cls.NUM_UNITS}"

        return cls(name=name, level=level, health=health, power=power, attack_range=attack_range, speed=speed)

    @property
    def short_text(self) -> str:
        return "A"

class Swordsman(MeleeAttack, ArmoredDefense, Enemy):
    """Swordsmen are a type of enemy that have melee attack and armored defense"""
    NUM_UNITS = 0
    BASE_HEALTH = 4
    BASE_ARMOR = 1
    BASE_POWER = 3
    BASE_SPEED = 1

    @classmethod
    def create(cls, level: int) -> "Swordsman":
        """Create a Swordsman of the specified level"""
        health = ceil(cls.BASE_HEALTH * level * 1.1)
        armor = ceil(cls.BASE_ARMOR + level * .2)
        power = cls.BASE_POWER + level
        speed = ceil(cls.BASE_SPEED + level * .05)
        cls.NUM_UNITS += 1
        name = f"{cls.__name__} {cls.NUM_UNITS}"

        return cls(name=name, level=level, health=health, power=power, armor=armor, speed=speed)

    @property
    def short_text(self) -> str:
        return "S"

class Apprentice(MagicAttack, Barrier, Enemy):
    """Apprentices are a type of enemy that have magic attack and a barrier defense"""
    NUM_UNITS = 0
    BASE_HEALTH = 4
    BASE_RANGE = 2
    BASE_POWER = 3
    BASE_SPEED = 1
    BASE_ARMOR = 1

    @classmethod
    def create(cls, level: int) -> "Apprentice":
        """Creates a new Apprentice of the specified level"""
        health = ceil(cls.BASE_HEALTH * level * .8)
        attack_range = ceil(cls.BASE_RANGE + level * .25)
        power = cls.BASE_POWER + level * 1.1
        speed = ceil(cls.BASE_SPEED + level * .08)
        armor = level * cls.BASE_ARMOR
        cls.NUM_UNITS += 1
        name = f"{cls.__name__} {cls.NUM_UNITS}"

        return cls(name=name, level=level, health=health, power=power, attack_range=attack_range, speed=speed, armor=armor)

    @property
    def short_text(self):
        return "M"

class Army(Enemy):
    """
    An army is made of one or more units, and in turn, behaves like a single unit, meaning
    that it can move, attack, receive damage, etc. In general, some special behaviour applies,
    for instance:
    - The army's health is the sum of the health of all units in it
    - The army's speed is the speed of the slowest unit in the army
    - When the army moves, the position of all units in the army will be updated too.
    - When the army attacks, all units in the army will try to attack the target
    - When the army is attacked, the first unit in the army will take the damage.
    """
    def __init__(self, units: List[Enemy], **kwargs):
        self.units = units
        self._position = None

        # Both speed and level are calculated, we just set a dummy value here
        super().__init__(speed=0, level=0, **kwargs)

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, position: Position):
        self._position = position

        for unit in self.units:
            unit.position = position

    @property
    def health(self) -> int:
        return sum(map(lambda u: u.health, self.units))

    @property
    def speed(self):
        return min(map(lambda u: u.speed, self.units))

    @speed.setter
    def speed(self, speed: int):
        pass

    @property
    def level(self) -> int:
        return sum(map(lambda u: u.level, self.units))

    @level.setter
    def level(self, level: int):
        pass

    def __add__(self, other: Unit) -> Unit:
        other.position = self.position
        self.units.append(other)
        return self

    def attack(self, target: Unit) -> bool:
        for unit in self.units:
            unit.attack(target)
            if not target.is_alive:
                return True

        return False

    def take_damage(self, damage: int) -> bool:
        if self.units[0].take_damage(damage):
            self.log(f"{self.units[0].name} has been destroyed!")
            self.units.pop(0)

        if not self.is_alive:
            self.log("All units in the army have been destroyed!")

        # Result should be true when unit has been destroyed
        return not self.is_alive

    @property
    def short_text(self) -> str:
        return "R"

    @property
    def is_alive(self) -> bool:
        return any(self.units)