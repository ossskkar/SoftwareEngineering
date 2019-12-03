from enum import Enum
from typing import List, Optional

from .logger import Logger
from .hero import Hero
from .types import Position
from .board import Board
from .enemy import Enemy


class GameActions(Enum):
    """Holds the different actions that can be taken in the game"""
    MOVE_UP = "Move up"
    MOVE_DOWN = "Move down"
    MOVE_LEFT = "Move left"
    MOVE_RIGHT = "Move right"
    ATTACK = "Attack"
    EXIT = "Exit"

class GameStatus(Enum):
    """Represents the game status"""
    PLAYING = "Playing"
    GAME_OVER = "Game Over!"
    WON = "You Won!"


class Game(Logger):
    """This class puts together all the different pieces (the hero, board, enemies, etc), and implements
    all the logic required for these pieces to work together, such as determining what actions are available
    for the hero at every moment or performing the actions and updating the board accordingly."""
    def __init__(self, hero: Hero, width: int, height: int, num_enemies: int, min_level: int=1, max_level: int=3, board_cls: type = Board, **kwargs):
        self.hero = hero
        self.board = board_cls.create(hero=hero, width=width, height=height, num_enemies=num_enemies, min_level=min_level, max_level=max_level)
        self.status = GameStatus.PLAYING
        super().__init__(name="game", *kwargs)

    def available_actions(self) -> List[GameActions]:
        """
        Calculates the available actions.
        - For the movement actions, the hero will be able to move up/down/left/right if the target position is valid and empty.
        - The attack action will be available if the hero has enemies within its attack range.
        - Finally, the exit action will be available if the exit portal is within the movement range of the hero.

        Note that if the game is in a status other than PLAYING, no action can be taken.
        """
        if self.status != GameStatus.PLAYING:
            return []

        available_actions = []
        current_pos = self.hero.position
        up    = Position(x=current_pos.x, y=current_pos.y+1)
        down  = Position(x=current_pos.x, y=current_pos.y-1)
        left  = Position(x=current_pos.x-1, y=current_pos.y)
        right = Position(x=current_pos.x+1, y=current_pos.y)
        if hasattr(self.hero, 'attack_range'):
            dist = self.hero.attack_range
        else:
            dist = 1

        can_attack = self.board.has_enemies_in_range(self.hero.position, dist)

        if self.board.is_valid(up):
            available_actions.append(GameActions.MOVE_UP)

        if self.board.is_valid(down):
            available_actions.append(GameActions.MOVE_DOWN)

        if self.board.is_valid(left):
            available_actions.append(GameActions.MOVE_LEFT)

        if self.board.is_valid(right):
            available_actions.append(GameActions.MOVE_RIGHT)

        exit_position = Position(x=self.board.width - 1, y=self.board.height - 1)

        if self.hero.position.distance(exit_position) <= self.hero.speed:
            available_actions.append(GameActions.EXIT)

        if can_attack:
            available_actions.append(GameActions.ATTACK)

        return available_actions

    def do(self, action: GameActions, target: Optional[Position]=None) -> bool:
        """Performs an action. This method has two main parts:
        - Check that the requested action can be taken, meaning that it is an available action,
          and that any extra parameters (e.g. the target of the attack) are also provided
        - If the action is valid, perform it and update the different game elements (e.g. remove
          units that have been destroyed, update positions in the board, etc)"""
        if self.status != GameStatus.PLAYING:
            self.log("The game has already finished, you can't keep playing!")
            return False
        elif action not in self.available_actions():
            self.log(f"Action {action.value} is not available right now")
            return False
        elif GameActions.ATTACK == action and target is None:
            self.log(f"Action {action.value} requires a target position!")
            return False
        elif GameActions.ATTACK == action and not self.board.is_enemy(target):
            self.log(f"Action {action.value} requires an enemy in the target position!")
            return False
        elif GameActions.EXIT == action:
            self.log("You won!")
            self.status = GameStatus.WON
            return True

        current_pos = self.hero.position

        if GameActions.ATTACK == action:
            result = self._attack(target)
            if not self.hero.is_alive:
                self.status = GameStatus.GAME_OVER
                self.log("You died, game over!")
            return result
        elif GameActions.MOVE_UP == action:
            new_pos = Position(x=current_pos.x, y=current_pos.y+1)
        elif GameActions.MOVE_DOWN == action:
            new_pos = Position(x=current_pos.x, y=current_pos.y-1)
        elif GameActions.MOVE_LEFT == action:
            new_pos = Position(x=current_pos.x-1, y=current_pos.y)
        else:
            new_pos = Position(x=current_pos.x+1, y=current_pos.y)

        return self.board.move(unit=self.hero, destination=new_pos)

    def _attack(self, position: Position) -> bool:
        enemy = self.board.get(position)
        self.hero.attack(enemy)

        if not enemy.is_alive:
            self.hero.heal()
            self.board.clear(position)
            return self.board.move(unit=self.hero, destination=position)
        else:
            self.log(f"Enemy {enemy.name} is retaliating against the hero!")
            enemy.attack(self.hero)
            return True
