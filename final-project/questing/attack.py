from abc import ABC, abstractmethod
import math

from .logger import Logger


class Attack(ABC, Logger):
    """
    This is the interface for game elements that can attack other units.
    """
    def __init__(self, power: int, **kwargs):
        super().__init__(**kwargs)
        self.power = power

    @abstractmethod
    def attack(self, target: "Unit") -> bool: # pragma: no cover
        """Attacks another unit. The result of this method should be True when the other unit
        is destroyed as a consequence of the attack"""
        pass

class MeleeAttack(Attack):
    """
    This type of attack represents close range attacks, meaning that this type of attack
    can only reach targets at a distance of 1.
    """
    def attack(self, target: "Unit") -> bool:
        distance = self.position.distance(target.position)

        if distance > 1:
            self.log("Target is out of reach, can't attack!")
            return False
        else:
            self.log(f"Attacking {target.name}!")
            return target.take_damage(self.power)

class RangedAttack(Attack):
    """
    Ranged attacks can hit targets that are within range.
    However, when the target is too close, attacks happen with half of the power instead.
    """
    def __init__(self, attack_range: int, **kwargs):
        super().__init__(**kwargs)
        self.attack_range = attack_range

    def attack(self, target: "Unit") -> bool:
        distance = self.position.distance(target.position)

        if distance > self.attack_range:
            self.log("Target is out of reach, can't attack!")
            return False

        power = self.power

        if distance <= 1:
            self.log("Target is too close, will attack with half power")
            power = self.melee_range_power


        self.log(f"Attacking {target.name} with power {power}")

        return target.take_damage(power)

    @property
    def melee_range_power(self) -> int:
        return math.ceil(self.power / 2)

class MagicAttack(RangedAttack):
    """
    Magic attacks are just like ranged attacks, except that they don't suffer the
    power penalty when they attack at short range.
    """
    @property
    def melee_range_power(self) -> int:
        return self.power
