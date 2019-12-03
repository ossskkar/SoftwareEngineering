from typing import Optional

from .unit import Unit
from .attack import MagicAttack, MeleeAttack, RangedAttack
from .defense import ArmoredDefense, Barrier, Defense
from .types import Position

class Hero(Unit):
    """Base class for heroes, which the players will control."""
    @property
    def short_text(self):
        return "H"

class Warrior(MeleeAttack, ArmoredDefense, Hero):
    """Warriors are heroes with melee attack and armored defense"""
    def __init__(self, name: str, position: Optional[Position] = None):
        name += ' - Warrior'
        super().__init__(name=name, power=4, armor=1, speed=1, health=10, position=position)

class Rogue(RangedAttack, Defense, Hero):
    """Rogues have a ranged attack but no extra defense"""
    def __init__(self, name: str, position: Optional[Position] = None):
        name += ' - Rogue'
        super().__init__(name=name, power=3, attack_range=3, speed=2, health=9, position=position)

class Mage(MagicAttack, Barrier, Hero):
    """Mages have a magic attack, and a barrier, meaning that they absorb the first points of
    damage they receive"""
    def __init__(self, name: str, position: Optional[Position] = None):
        name += ' - Mage'
        super().__init__(name=name, power=3, armor=2, attack_range=2, speed=1, health=8, position=position)
