from typing import List, Optional

import numpy as np

from .hero import Hero
from .logger import Logger
from .types import Position
from .enemy import Enemy
from .game_element import ExitPortal


class Board(Logger):
    """
    The game board. It contains the units, and all the logic to move them around the board.
    """
    def __init__(self, width: int, height: int, **kwargs):
        super().__init__(name='board', **kwargs)

        self.width = width
        self.height = height

        self._board = np.full(shape=(width, height), fill_value=None, dtype=object)

    @property
    def num_empty_slots(self) -> int:
        """Returns the number of empty positions in the board"""
        return sum(sum(self._board == None))

    @property
    def empty_slots(self) -> List[Position]:
        """Returns all the empty positions in the board"""
        empty_slots = np.argwhere(self._board == None)

        empty_slots = list(map(lambda s: Position(x=s[0], y=s[1]), empty_slots))

        return empty_slots

    def __getitem__(self, position: Position) -> Optional["GameElement"]:
        """Allows to access positions by using board[position] instead of board.get(position)"""
        return self._board[position]

    def get(self, position: Position) -> Optional["GameElement"]:
        """Returns the game element at a certain position in the board.
        Note that the position might be empty; in such case, None will be returned."""
        return self._board[position]

    def move(self, unit: "Unit", destination: Position) -> bool:
        """Moves the unit to the given position. It returns True if the move is successful,
        False otherwise (e.g. if the position is not valid, occupied or out of range)."""
        current_position = unit.position

        if not self.is_valid(destination):
            self.log(f"Target position {destination} is not valid!")
            return False
        elif not self.is_empty(destination):
            self.log(f"Can't move {unit.name} to position {destination}, it's not empty!")
            return False
        elif unit.move(destination):
            self.clear(current_position)
            self._board[destination] = unit
            self.log(f"Moved {unit.name} from {current_position} to position {destination}")
            return True
        else:
            self.log(f"Failed to move {unit.name} to position {destination}")
            return False

    def place(self, element: "GameElement", destination: Position) -> bool:
        """Places an element in the board. Note that the main difference is that this method
        does not depend on the ability of the element/unit to move."""
        if not self.is_valid(destination):
            self.log(f"Target position {destination} is not valid!")
            return False
        elif not self.is_empty(destination):
            self.log(f"Can't place element {element.name} at position {destination}, it's not empty!")
            return False

        element.position = destination
        self._board[destination] = element
        self.log(f"Placed {element.name} at position {destination}")

        return True

    def clear(self, position: Optional[Position] = None) -> bool:
        """Clears a position in the board. This method is useful, e.g. when a unit has been destroyed."""
        if position is None:
            return False
        elif not self.is_valid(position):
            self.log(f"Can't clear position {position}, it's not valid!")
            return False

        self._board[position] = None

        return True

    def is_empty(self, position: Position) -> bool:
        """Checks whether a position in the board is empty"""
        return self._board[position] is None

    def is_enemy(self, position: Position) -> bool:
        """Checks whether a position in the board contains an enemy"""
        return isinstance(self._board[position], Enemy)

    def is_valid(self, position: Position) -> bool:
        """Checks whether a position is a valid position in the board,
        meaning that it should be within the boundaries of the board."""
        return position.x >= 0 and position.x < self.width \
               and position.y >= 0 and position.y < self.height

    def has_enemies_in_range(self, position: Position, distance: int) -> bool:
        """This method checks if there are enemies at the specified distance,
        starting from the position provided. It can be used to determine whether
        an attack action can be taken or not."""
        start_x = max(0, position.x - distance)
        end_x   = min(self.width - 1, position.x + distance) + 1
        start_y = max(0, position.y - distance)
        end_y   = min(self.height - 1, position.y + distance) + 1

        x_range = range(start_x, end_x)
        y_range = range(start_y, end_y)
        positions = [Position(x=x, y=y) for x in x_range for y in y_range]

        def position_has_enemy(pos: Position) -> bool:
            return pos != position \
                and position.distance(to=pos) <= distance \
                and self.is_enemy(pos)

        positions = list(filter(position_has_enemy, positions))
        self.log(f"Positions with enemies in attack range: {positions}")

        return any(positions)

    def get_empty_slot(self) -> Optional[Position]:
        """Gets a random empty slot from the board, if there are any."""
        if not self.num_empty_slots:
            self.log("No more empty positions in the board!")
            return None

        empty_slots = self.empty_slots
        slot_idx = np.random.randint(len(empty_slots))

        return empty_slots[slot_idx]

    @classmethod
    def create(cls, hero: Hero, width: int, height: int, num_enemies: int, min_level=1, max_level=3):
        """Creates a board with the given width, height and number of enemies. The hero will always
        be placed at position (0, 0), and the exit portal will be placed in the opposite corner."""
        board = cls(width=width, height=height)
        board.place(hero, destination=Position(0, 0))

        exit_portal = ExitPortal()
        board.place(exit_portal, destination=Position(width - 1, height - 1))

        # Make sure that we don't create more enemies than slots
        num_enemies = min(num_enemies, board.num_empty_slots)

        for _ in range(num_enemies):
            pos = board.get_empty_slot()
            level = np.random.randint(min_level, max_level + 1)
            enemy = Enemy.random_enemy(level)
            board.place(enemy, destination=pos)

        return board
