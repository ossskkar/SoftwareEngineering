import pytest
import numpy as np
from unittest import mock

from questing import Board
from questing import Position
from questing import GameElement, Unit, Enemy, Hero


def EMPTY_BOARDS():
    return [
        Board(width=2, height=2),
        Board(width=4, height=4),
        Board(width=8, height=5),
        Board(width=3, height=6),
    ]

@pytest.fixture
def board():
    return Board(width=5, height=5)

@pytest.fixture
def unit():
    unit = mock.MagicMock(spec=Unit)
    unit.name = "Test unit"
    unit.position = Position(0, 0)

    return unit

@pytest.fixture
def game_element():
    element = mock.MagicMock(spec=GameElement)
    element.name = "Game Element"

    return element

@pytest.fixture
def enemy():
    enemy = mock.MagicMock(spec=Enemy)
    enemy.name = "Enemy"

    return enemy

@pytest.fixture
def hero():
    hero = mock.MagicMock(spec=Hero)
    hero.name = "Hero"

    return hero

def test_board_has_width_and_height():
    width = 5
    height = 3

    board = Board(width=width, height=height)

    assert hasattr(board, "width"), f"Board should have a width attribute"
    assert board.width == width, f"Board should have a width of {width}"
    assert hasattr(board, "height"), f"Board should have a height attribute"
    assert board.height == height, f"Board should have a height of {height}"

@pytest.mark.parametrize("board", EMPTY_BOARDS())
def test_num_empty_slots(board):
    expected_slots = board.width * board.height

    assert board.num_empty_slots == expected_slots, \
        f"An empty board of {board.width}x{board.height} should have {expected_slots} empty slots"

@pytest.mark.parametrize("board", EMPTY_BOARDS())
def test_empty_slots(board):
    expected_positions = [Position(x, y) for x in range(board.width) for y in range(board.height)]

    assert sorted(board.empty_slots) == sorted(expected_positions), \
        f"The board doesn't have all the expected empty slots"

@pytest.mark.parametrize("board", EMPTY_BOARDS())
def test_getitem(board):
    element = mock.MagicMock()
    position = Position(0, 0)

    board.place(element, destination=position)

    assert board[position] == element, f"board[{position}] did not contain the expected element"

@pytest.mark.parametrize("board", EMPTY_BOARDS())
def test_get(board):
    element = mock.MagicMock()
    position = Position(0, 0)

    board.place(element, destination=position)

    assert board.get(position) == element, f"board.get({position}) did not contain the expected element"

def test_move_to_invalid_position(capsys, board, unit):
    destination = Position(board.width + 1, 0)
    expected_msg = f"Target position {destination} is not valid!"

    result = board.move(unit, destination=destination)
    out, _ = capsys.readouterr()

    assert result == False, f"Moving to invalid position {destination} should return false"
    assert expected_msg in out

def test_move_to_non_empty_position(capsys, board, unit):
    other_unit = mock.MagicMock()
    destination = Position(1, 0)

    board.place(other_unit, destination)
    expected_msg = f"Can't move {unit.name} to position {destination}, it's not empty!"

    result = board.move(unit, destination=destination)
    out, _ = capsys.readouterr()

    assert result == False, f"Moving to occupied position {destination} should return false"
    assert expected_msg in out

def test_move_when_move_fails(capsys, board, unit):
    unit.move.return_value = False
    destination = Position(0, 0)
    expected_msg = f"Failed to move {unit.name} to position {destination}"

    result = board.move(unit, destination=destination)
    out, _ = capsys.readouterr()

    assert result == False, f"board.move should return False if the unit.move fails"
    assert expected_msg in out
    unit.move.assert_called_once_with(destination)

def test_move(capsys, board, unit):
    unit.move.return_value = True
    origin = unit.position
    destination = Position(1, 1)
    expected_msg = f"Moved {unit.name} from {origin} to position {destination}"

    result = board.move(unit, destination=destination)
    out, _ = capsys.readouterr()

    assert result == True, f"board.move should return True if the unit.move succeeds"
    assert board.get(origin) == None, f"Origin position {origin} should be empty after moving"
    assert board.get(destination) == unit, f"Unit should be in the destination {destination}"
    assert expected_msg in out
    unit.move.assert_called_once_with(destination)

def test_place_at_invalid_position(capsys, board, unit):
    destination = Position(board.width + 1, 0)
    expected_msg = f"Target position {destination} is not valid!"

    result = board.place(unit, destination=destination)
    out, _ = capsys.readouterr()

    assert result == False, f"Placing an element at an invalid position should return false"
    assert expected_msg in out

def test_place_at_non_empty_position(capsys, board, unit):
    other_unit = mock.MagicMock()
    destination = Position(1, 0)

    board.place(other_unit, destination)
    expected_msg = f"Can't place element {unit.name} at position {destination}, it's not empty!"

    result = board.place(unit, destination=destination)
    out, _ = capsys.readouterr()

    assert result == False, f"Placing an element in a occupied position should return false"
    assert expected_msg in out

def test_clear_no_position(board):
    result = board.clear(position=None)

    assert result == False, f"board.clear with no position should return False"

def test_clear_invalid_position(capsys, board):
    position = Position(10, 10)
    expected_msg = f"Can't clear position {position}, it's not valid!"

    result = board.clear(position=position)
    out, _ = capsys.readouterr()

    assert result == False, f"board.clear with invalid position {position} should return False"
    assert expected_msg in out

def test_clear(board, unit):
    position = Position(1, 1)
    board.place(unit, destination=position)

    result = board.clear(position=position)

    assert result == True, f"board.clear({position}) should return True"

@pytest.mark.parametrize("empty_board", EMPTY_BOARDS())
def test_is_empty(empty_board):
    pos = Position(0, 0)

    result = empty_board.is_empty(pos)

    assert result == True, f"Position {pos} should be empty"

def test_is_enemy_empty_position(board):
    position = Position(0, 0)

    is_enemy = board.is_enemy(position)

    assert is_enemy == False, f"Empty position {position} is not an enemy"

def test_is_enemy_with_game_element(board, game_element):
    position = Position(0, 0)
    board.place(game_element, position)

    is_enemy = board.is_enemy(position)

    assert is_enemy == False, f"Game element at {position} is not an enemy"

def test_is_enemy_with_enemy(board, enemy):
    position = Position(0, 0)
    board.place(enemy, position)

    is_enemy = board.is_enemy(position)

    assert is_enemy == True, f"Game element at {position} is an enemy"


def _create_board_with_enemies(width: int, height: int, *enemy_positions: Position):
    board = Board(width=width, height=height)

    for idx, enemy_position in enumerate(enemy_positions):
        enemy = mock.MagicMock(spec=Enemy)
        enemy.name = f"Enemy {idx + 1}"
        board.place(enemy, enemy_position)

    return board


def BOARD_WITH_ENEMIES():
    fixtures = []
    width = 10
    height = 10

    # Cases at range 1
    board = _create_board_with_enemies(width, height, Position(5, 5))
    distance = 1

    from_pos = Position(0, 0)
    expected_result = False
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(4, 4)
    expected_result = False
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(4, 6)
    expected_result = False
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(6, 4)
    expected_result = False
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(6, 6)
    expected_result = False
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(4, 5)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(6, 5)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(5, 4)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(5, 6)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    # Cases at range 2
    distance = 2

    from_pos = Position(0, 0)
    expected_result = False
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(4, 4)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(4, 6)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(6, 4)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(6, 6)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(4, 5)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(6, 5)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(5, 4)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(5, 6)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(5, 7)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(7, 6)
    expected_result = False
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(7, 7)
    expected_result = False
    fixtures.append((board, from_pos, distance, expected_result))

    # Test with a range that can cover the whole board (i.e. width + height)
    distance = width + height

    from_pos = Position(0, 0)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    from_pos = Position(width - 1, height - 1)
    expected_result = True
    fixtures.append((board, from_pos, distance, expected_result))

    return fixtures

@pytest.mark.parametrize("board,position,distance,expected_result", BOARD_WITH_ENEMIES())
def test_has_enemies_in_range(board, position, distance, expected_result):
    result = board.has_enemies_in_range(position=position, distance=distance)

    assert result == expected_result, f"Expected result for board.has_enemies_in_range with distance of {distance}: {expected_result}. Actual result: {result}"

def _get_full_board(width, height):
    b = Board(width=width, height=height)

    for x in range(width):
        for y in range(height):
            enemy = mock.MagicMock(spec=Enemy)
            enemy.name = f"Enemy x={width}, y={height}"
            pos = Position(x, y)
            b.place(enemy, pos)

    return b

def FULL_BOARDS():
    return [
        _get_full_board(width=2, height=2),
        _get_full_board(width=4, height=4),
        _get_full_board(width=8, height=5),
        _get_full_board(width=3, height=6),
    ]

@pytest.mark.parametrize("board", FULL_BOARDS())
def test_get_empty_slot_with_full_board(board, capsys):
    expected_msg = "No more empty positions in the board!"

    result = board.get_empty_slot()
    out, _ = capsys.readouterr()

    assert result is None, f"There should be no empty slots in the board!"
    assert expected_msg in out

@pytest.mark.parametrize("board", EMPTY_BOARDS())
def test_get_empty_slot(board):
    empty_slots = board.empty_slots

    idx = np.random.randint(len(empty_slots))

    with mock.patch("numpy.random.randint", return_value=idx):
        result = board.get_empty_slot()

    assert result == empty_slots[idx], f"The returned empty slot should have been the one at index {idx}: Position{empty_slots[idx]}"

def test_create(hero, board):
    width = board.width
    height = board.height
    board.place(hero, Position(0, 0))
    num_enemies = 3
    min_level = 1
    max_level = 5
    # We'll be creating a board of the same width and height, so initially the empty slots will be the same
    empty_slots = board.empty_slots
    expected_enemy_positions = []
    enemies = []

    def create_enemy(level):
        enemy = mock.MagicMock(spec=Enemy)
        enemy.name = f"Enemy {len(enemies) + 1}"
        # Add the expected position and enemy to the lists, so that we can check later
        expected_enemy_positions.append(empty_slots.pop(0))
        enemies.append(enemy)

        return enemy

    with mock.patch("questing.Enemy.random_enemy", side_effect=create_enemy) as rand_enemy:
        # For every enemy, there are two calls to np.random.randint
        # The first one is to determine the empty slot index, while
        # the second one is to determine the level of the enemy created.
        with mock.patch("numpy.random.randint", side_effect=[0, 1, 0, 2, 0, 3]):
            generated_board = Board.create(hero=hero, width=width, height=height, num_enemies=num_enemies, min_level=min_level, max_level=max_level)

    assert generated_board.width == width, f"Generated board should have a width of {width}"
    assert generated_board.height == height, f"Generated board should have a height of {height}"
    assert generated_board.get(Position(0, 0)) == hero, f"Hero should be placed in position (0, 0) in the board"

    rand_enemy.assert_has_calls([mock.call(1), mock.call(2), mock.call(3)])
    for idx, pos in enumerate(expected_enemy_positions):
        assert generated_board.is_enemy(pos), f"There should be an enemy at position {pos}"
        assert generated_board.get(pos) == enemies[idx], f"Enemy at position {pos} should be {enemies[idx].name}"
