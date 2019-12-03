import pytest

from unittest import mock

from questing import Board
from questing import Game, GameStatus, GameActions
from questing import Hero
from questing import Position

@pytest.fixture
def hero():
    hero = mock.MagicMock(spec=Hero)
    hero.name = "TestHero"
    hero.speed = 1
    hero.position = Position(0, 0)

    return hero

@pytest.fixture
def board():
    board = mock.MagicMock(spec=Board)
    board.create = mock.MagicMock(return_value=board)

    return board

@pytest.fixture
def board_cls(board):
    board_cls = mock.MagicMock()

    board_cls.create = mock.MagicMock(return_value=board)
    board_cls._board_mock = board

    return board_cls
@pytest.fixture
def game(hero, board_cls):
    return get_game(hero=hero, board_cls=board_cls)

def get_game(hero: Hero, board_cls: Board, width: int = 4, height: int = 4, num_enemies: int = 4, min_level: int=1, max_level: int=3):
    board_cls._board_mock.width = width
    board_cls._board_mock.height = height

    return Game(hero=hero, board_cls=board_cls, width=width, height=height, num_enemies=num_enemies, min_level=min_level, max_level=max_level)

def test_game_creation_sets_hero(hero, board_cls):
    game = get_game(hero=hero, board_cls=board_cls)

    assert game.hero == hero, f"Game hero should be set"

def test_game_creation_sets_board(hero, board_cls, board):
    board_width = 3
    board_height = 4
    num_enemies = 2
    min_level = 2
    max_level = 10
    game = get_game(hero=hero, board_cls=board_cls, width=board_width, height=board_height, num_enemies=num_enemies, min_level=min_level, max_level=max_level)

    assert game.board == board, f"Game board should be set"
    board_cls.create.assert_called_once_with(hero=hero, width=board_width, height=board_height, num_enemies=num_enemies, min_level=min_level, max_level=max_level)

def test_game_starts_in_playing_status(hero, board_cls):
    game = get_game(hero=hero, board_cls=board_cls)

    assert game.status == GameStatus.PLAYING, f"Game status should be GameStatus.PLAYING"

# Tests for available actions

def test_available_actions_with_game_finished(game):
    game.status = GameStatus.WON

    available_actions = game.available_actions()

    assert available_actions == [], f"There should be no actions when game is not in PLAYING status"

def test_available_actions_with_move_up(game, board, hero):
    up_position = Position(0, 1)

    board.is_valid.return_value = True

    available_actions = game.available_actions()

    assert GameActions.MOVE_UP in available_actions, f"GameActions.MOVE_UP should be in the available actions"
    board.is_valid.assert_any_call(up_position)

def test_available_actions_with_move_up_not_valid(game, board, hero):
    up_position = Position(0, 1)

    board.is_valid.return_value = False

    available_actions = game.available_actions()

    assert GameActions.MOVE_UP not in available_actions, f"GameActions.MOVE_UP should be in the available actions"
    board.is_valid.assert_any_call(up_position)

def test_available_actions_with_enemies_in_range(game, board, hero):
    board.is_valid.return_value = False

    board.has_enemies_in_range.return_value = True
    available_actions = game.available_actions()

    assert GameActions.ATTACK in available_actions, f"GameActions.ATTACK should be in the available actions"
    board.has_enemies_in_range.assert_called_once_with(hero.position, 1)

def test_available_actions_with_enemies_not_in_range(game, board, hero):
    board.is_valid.return_value = False

    board.has_enemies_in_range.return_value = False
    available_actions = game.available_actions()

    assert GameActions.ATTACK not in available_actions, f"GameActions.ATTACK should not be in the available actions"
    board.has_enemies_in_range.assert_called_once_with(hero.position, 1)

def test_available_actions_with_ranged_attack(game, board, hero):
    hero.attack_range = 3
    board.is_valid.return_value = False

    board.has_enemies_in_range.return_value = True
    available_actions = game.available_actions()

    assert GameActions.ATTACK in available_actions, f"GameActions.ATTACK should be in the available actions"
    board.has_enemies_in_range.assert_called_once_with(hero.position, 3)

def test_available_actions_corner(game, board, hero):
    up_position = Position(0, 1)
    right_position = Position(1, 0)
    down_position = Position(0, -1)
    left_position = Position(-1, 0)

    valid_positions = [up_position, right_position]

    def is_valid_side_effect(pos):
        return pos in valid_positions

    board.is_valid.side_effect = is_valid_side_effect
    board.has_enemies_in_range.return_value = False

    expected_actions = [GameActions.MOVE_UP, GameActions.MOVE_RIGHT]

    available_actions = game.available_actions()

    assert len(available_actions) == len(expected_actions), f"There should be {len(expected_actions)} available actions, but there are {len(available_actions)}"
    for e in expected_actions:
        assert e in available_actions, f"{e} should be an available action!"

    board.is_valid.assert_any_call(up_position)
    board.is_valid.assert_any_call(down_position)
    board.is_valid.assert_any_call(right_position)
    board.is_valid.assert_any_call(left_position)
    board.has_enemies_in_range.assert_called_once_with(hero.position, 1)

def test_available_actions_with_exit_portal(game, board, hero):
    # This is just to make sure that the exit is reachable, usually having a speed of width + height guarantees that you can reach it.
    hero.speed = 100000

    board.is_valid.return_value = False
    board.has_enemies_in_range.return_value = False

    available_actions = game.available_actions()

    assert GameActions.EXIT in available_actions, f"GameActions.EXIT should be in the available actions"

# Tests for the "do" method

@pytest.fixture(params=[s for s in GameStatus if s != GameStatus.PLAYING])
def non_playable_status(request):
    return request.param

def test_do_not_playing(capsys, game, non_playable_status):
    game.status = GameStatus.GAME_OVER

    msg = "The game has already finished, you can't keep playing!"
    expected_msg = f"[{game.__class__.__name__}] {msg}"

    result = game.do(GameActions.MOVE_UP)
    out, _ = capsys.readouterr()

    assert result == False, f"game.do should return False when status is {non_playable_status}"
    assert expected_msg.lower() in out.lower()

def test_do_unavailable_action(capsys, game, hero, board):
    board.has_enemies_in_range.return_value = False
    action = GameActions.ATTACK

    msg = f"Action {action.value} is not available right now"
    expected_msg = f"[{game.__class__.__name__}] {msg}"

    result = game.do(action)

    out, _ = capsys.readouterr()

    assert result == False, f"game.do should return False when action is not in available_actions"
    assert expected_msg.lower() in out.lower()

def test_attack_with_no_target(capsys, game, hero, board):
    action = GameActions.ATTACK
    board.has_enemies_in_range.return_value = True

    msg = f"Action {action.value} requires a target position!"
    expected_msg = f"[{game.__class__.__name__}] {msg}"

    result = game.do(action)

    out, _ = capsys.readouterr()

    assert result == False, f"game.do should return False when attacking with no target provided"
    assert expected_msg.lower() in out.lower()

def test_attack_with_target_position_empty(capsys, game, hero, board):
    action = GameActions.ATTACK
    target = Position(2, 2)
    board.has_enemies_in_range.return_value = True
    board.is_enemy.return_value = False

    msg = f"Action {action.value} requires an enemy in the target position!"
    expected_msg = f"[{game.__class__.__name__}] {msg}"

    result = game.do(action, target=target)

    out, _ = capsys.readouterr()

    assert result == False, f"game.do should return False when attacking a non-enemy position"
    assert expected_msg.lower() in out.lower()

def test_exit(capsys, game, hero, board):
    action = GameActions.EXIT
    hero.speed = 1000

    msg = "You won!"
    expected_msg = f"[{game.__class__.__name__}] {msg}"

    result = game.do(action)

    out, _ = capsys.readouterr()

    assert result == True, f"game.do should return True when exiting the dungeon"
    assert expected_msg.lower() in out.lower()

def test_attack_enemy_not_killed(capsys, game, hero, board):
    hero.is_alive = True
    action = GameActions.ATTACK
    target = Position(2, 2)
    board.has_enemies_in_range.return_value = True
    board.is_enemy.return_value = True
    enemy = mock.MagicMock()
    enemy.is_alive = True
    enemy.name = "Foo"
    board.get.return_value = enemy
    msg = f"Enemy {enemy.name} is retaliating against the hero!"
    expected_msg = f"[{game.__class__.__name__}] {msg}"

    result = game.do(action, target=target)
    out, _ = capsys.readouterr()

    assert result == True, "game.do should return True when attacking but not killing an enemy"
    hero.attack.assert_called_once_with(enemy)
    enemy.attack.assert_called_once_with(hero)
    assert expected_msg.lower() in out.lower()

def test_attack_enemy_not_killed_and_hero_killed(capsys, game, hero, board):
    hero.is_alive = False
    action = GameActions.ATTACK
    target = Position(2, 2)
    board.has_enemies_in_range.return_value = True
    board.is_enemy.return_value = True
    enemy = mock.MagicMock()
    enemy.is_alive = True
    enemy.name = "Foo"
    board.get.return_value = enemy
    msgs = [
        f"Enemy {enemy.name} is retaliating against the hero!",
        "You died, game over!",
    ]
    expected_msgs = [f"[{game.__class__.__name__}] {msg}" for msg in msgs]

    result = game.do(action, target=target)
    out, _ = capsys.readouterr()

    assert result == True, "game.do should return True when attacking but not killing an enemy"
    assert game.status == GameStatus.GAME_OVER, "Game status should be GAME_OVER when the hero is killed"
    hero.attack.assert_called_once_with(enemy)
    enemy.attack.assert_called_once_with(hero)
    for expected_msg in expected_msgs:
        assert expected_msg.lower() in out.lower()

def test_attack_enemy_killed(capsys, game, hero, board):
    hero.is_alive = True
    hero.heal = mock.MagicMock()
    action = GameActions.ATTACK
    target = Position(2, 2)
    board.has_enemies_in_range.return_value = True
    board.is_enemy.return_value = True
    enemy = mock.MagicMock()
    enemy.is_alive = False
    enemy.name = "Foo"
    board.get.return_value = enemy
    board.move.return_value = True
    result = game.do(action, target=target)

    assert result == True, "game.do should return True when attacking and killing an enemy"
    hero.attack.assert_called_once_with(enemy)
    hero.heal.assert_called_once()
    enemy.attack.assert_not_called()
    board.clear.assert_called_once_with(target)
    board.move.assert_called_once_with(unit=hero, destination=target)

MOVE_POSITIONS = [
    # Action, hero position, new_position
    (GameActions.MOVE_UP, Position(0, 0), Position(0, 1)),
    (GameActions.MOVE_DOWN, Position(1, 4), Position(1, 3)),
    (GameActions.MOVE_RIGHT, Position(0, 0), Position(1, 0)),
    (GameActions.MOVE_LEFT, Position(3, 0), Position(2, 0)),
]

@pytest.fixture(params=MOVE_POSITIONS)
def move_action(request):
    return request.param

def test_move_actions(game, board, hero, move_action):
    action, hero_pos, expected_pos = move_action
    hero.position = hero_pos

    board.is_valid.return_value = True
    board.move.return_value = True

    result = game.do(action)

    assert result == True, f"game.do({action.value}) should return True"
    board.move.assert_called_once_with(unit=hero, destination=expected_pos)


# Exercise.
def test_available_actions_occupied_slot(game, board):
    # Define the "up" position
    #up = Position(...)

    # Have the board return True for ```is_valid``` and False for ```is_empty```.

    # Get the available actions
    available_actions = game.available_actions()

    # Assert that the move up action is not in the available actions
    # assert ...

