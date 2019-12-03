from abc import abstractmethod

from .game_element import GameElement
from .types import Position


class Unit(GameElement):
    """Base class for units, which includes enemies and heroes. The main characteristic of units is
    that they have a speed, so they can move around the board, and that they can attack other units
    and receive damage. In general, the attack and take damage method will be implemented by using
    one of the Attack classes (e.g. MeleeAttack, RangedAttack, etc...) and the take_damage by using
    one of the Defense classes"""
    def __init__(self, speed: int, **kwargs):
        super().__init__(**kwargs)
        self.speed = speed

    def move(self, destination: Position) -> bool:
        """Move the unit to the target positions. This method will check if the unit can actually move to
        the target position, which is only possible if the speed of the unit is greater than or equal to
        the distance between the current and the target position."""
        target_dist = self.position.distance(destination)

        if target_dist > self.speed:
            self.log(f"Target position {destination} is at a distance of {target_dist} and my speed is {self.speed}, I can't reach it!")
            return False
        else:
            self.log(f"Moving to new position ({destination})")
            self.position = destination
            return True

    def __str__(self) -> str:
        return self.short_text

    @abstractmethod
    def attack(self, target: "Unit") -> bool: # pragma: no cover
        pass

    @abstractmethod
    def take_damage(self, damage: int) -> bool: # pragma: no cover
        pass
