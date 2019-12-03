from questing import Game, GameActions, ExitPortal
from questing import Hero, Warrior, Rogue, Mage
from questing import Position
from questing import GameElement

ACTION_TO_STR = {a: a.value for a in GameActions}
STR_TO_ACTION = {a.value: a for a in GameActions}

from typing import Optional

class GameClient:
    def __init__(self, hero: Hero, board_width: int, board_height: int, num_enemies: int):
        self.hero = hero
        self.board_width = board_width
        self.board_height = board_height
        self.num_enemies = num_enemies
        self.game = Game(hero=hero, width=board_width, height=board_height, num_enemies=num_enemies)

    def _game_element_to_symbol(self, element: GameElement):
        if element is None:
            return " " * 4
        elif isinstance(element, ExitPortal):
            return "EXIT"
        else:
            return str(element).ljust(4)

    def print_board(self):
        print("=" * (self.board_width * 7 + 1))
        for y in range(self.board_height):

            row_idx = self.board_height - 1 - y
            str_row = []
            for x in range(self.board_width):
                str_row.append(self._game_element_to_symbol(self.game.board[x][row_idx]))
            str_row = "| " + " | ".join(str_row) + " |"
            print(str_row)
            print("-" * (self.board_width * 7 + 1))
        print("=" * (self.board_width * 7 + 1))

    def play(self, action: Optional[str] = None, target: Optional[Position] = None, show: bool = True):
        if action:
            print(f"Taking action {action}")
            self.game.do(STR_TO_ACTION[action], target)

        if show:
            self.print_board()
            print("Available actions:")
            available_actions = self.game.available_actions()
            print([v for k, v in ACTION_TO_STR.items() if k in available_actions])
