from abc import ABC, abstractmethod
import math
from typing import Optional

from .logger import Logger


class Defense(Logger):
    """Implements the basic interface for units that can be destroyed. Such units
    have a 'health' attribute, and can recive damage via the 'take_damage' method.
    Their health can also be restored via the 'heal' method."""
    def __init__(self, health: int, **kwargs):
        super().__init__(**kwargs)
        self.health = health
        self._original_health = health

    def heal(self, points: Optional[int] = None):
        """Restores the specified number of health points to the unit. If no points are
        provided, the health is restored to full health. Note that (at least in the default
        implementation), health can never be restored above the original amount."""
        if points:
            self.log(f"Restoring {points} points of health")
            # Prevent health from going over the original health
            new_health = min(self.health + points, self._original_health)
            self.log(f"Health after healing: {new_health} (before: {self.health})")
            self.health = new_health
        else:
            self.log(f"Restoring to full health ({self._original_health} points)")
            self.health = self._original_health

    def take_damage(self, damage: int) -> bool:
        """
        This is the method you should use to have the unit receive damage.
        It will return True if the unit has been destroyed (i.e. health is <= 0),
        or False otherwise.
        """
        self.health -= damage

        if self.health <= 0:
            self.log(f"I took {damage} damage, and I've been destroyed!")
            return True
        else:
            self.log(f"I took {damage} damage, I have {self.health} health points left")
            return False

    @property
    def is_alive(self) -> bool:
        """Property to check whether the unit is still alive (i.e. health > 0)"""
        return self.health > 0

class ArmoredDefense(Defense):
    """This type of defense represents the case where the unit is armored,
    so everytime the unit takes damage, part of it (or all of it!) is absorved."""
    def __init__(self, armor: int, **kwargs):
        super().__init__(**kwargs)
        self.armor = armor

    def take_damage(self, damage: int) -> bool:
        """In this case, everytime the unit takes damage, part of it will be
        absorved by its armor."""
        new_damage = self._absorb(damage)

        return super().take_damage(new_damage)

    def _absorb(self, damage: int) -> int:
        new_damage = max(damage - self.armor, 0)
        absorved_damage = min(damage, self.armor)
        self.log(f"Armor absorved {absorved_damage} damage, taking {new_damage} damage instead of {damage}")

        return new_damage

class Barrier(ArmoredDefense):
    """
    The Barrier defense is similar to the ArmoredDefense, with the exception that the armor breaks over time,
    and at some point the barrier will be broken. In other words, a barrier will absorb the N first points
    of damage, where N is the armor value.
    """
    def _absorb(self, damage: int) -> int:
        if not self.armor:
            return damage

        new_damage = super()._absorb(damage)

        self.armor = max(self.armor - damage, 0)

        if not self.armor:
            self.log("My armor has been broken!")

        return new_damage
