from abc import ABC, abstractmethod
from typing import Optional

from .logger import Logger
from .types import Position


class GameElement(ABC, Logger):
    """A game element is the base class for any object that can be placed on the board.
    Game elements can have a positions, and can be represented with a short text"""
    def __init__(self, position: Optional[Position] = None, **kwargs):
        super().__init__(**kwargs)
        self.position = position

    @property
    @abstractmethod
    def short_text(self) -> str: # pragma: no cover
        pass

class Wall(GameElement):
    """Walls are just static elements that can be placed in the board"""
    def __init__(self, **kwargs):
        super().__init__(name="Wall", **kwargs)

    @property
    def short_text(self):
        return "W"

class ExitPortal(GameElement):
    """The exit portal is where the heroes need to get to win the game,
    it's the exit from the dungeon."""
    def __init__(self, **kwargs):
        super().__init__(name="Exit portal", **kwargs)

    @property
    def short_text(self) -> str:
        return "EXIT"