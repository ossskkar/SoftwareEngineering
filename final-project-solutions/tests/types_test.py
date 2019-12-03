from typing import NamedTuple
import pytest

from questing import Position

def test_position_x_coordinate():
    x = 1

    pos = Position(x=x, y=0)

    assert pos.x == x, f"X position is {pos.x}, but it should be {x}"

def test_position_y_coordinate():
    y = 5

    pos = Position(x=0, y=y)

    assert pos.y == y, f"Y position is {pos.y}, but it should be {y}"

def test_position_can_be_compared_to_tuple():
    x = 1
    y = 5
    expected = (x, y)

    pos = Position(x=x, y=y)

    assert pos == expected, f"Position {pos} should be equal to tuple {expected}"

# EXERCISE.
DISTANCES = [
    # (from_pos, to_pos, distance)
    (Position(0, 0), Position(0, 1), 1),
    (Position(0, 0), Position(0, 2), 2),
    (Position(0, 0), Position(3, 0), 3),
    (Position(0, 0), Position(1, 1), 2),
    (Position(5, 4), Position(1, 2), 6),
    (Position(3, 7), Position(5, 7), 2),
    (Position(3, 1), Position(4, 8), 8),
]

@pytest.mark.parametrize("from_pos,to_pos,expected_distance", DISTANCES)
def test_distance(from_pos, to_pos, expected_distance):
    distance = from_pos.distance(to=to_pos)

    assert distance == expected_distance, \
        f"Distance from {from_pos} to {to_pos} was be {distance}, but should be {expected_distance}"
