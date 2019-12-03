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

"""
EXERCISE. Can you convert the tests below into a single parametrize test?

These are all the positions we want to test, and the expected distance:
- Format is (start_x, start_y), (end_x, end_y), distance
- (0, 0), (0, 1), 1
- (0, 0), (0, 2), 2
- (0, 0), (3, 0), 3
- (0, 0), (1, 1), 2
- (5, 4), (1, 2), 6
- (3, 7), (5, 7), 2
- (3, 1), (4, 8), 8
"""
def test_distance():
    from_pos = Position(0, 0)
    to_pos = Position(1, 1)
    expected_distance = 2

    distance = from_pos.distance(to=to_pos)

    assert distance == expected_distance, \
        f"Distance from {from_pos} to {to_pos} was be {distance}, but should be {expected_distance}"

def test_another_distance():
    from_pos = Position(5, 4)
    to_pos = Position(1, 2)
    expected_distance = 6

    distance = from_pos.distance(to=to_pos)

    assert distance == expected_distance, \
        f"Distance from {from_pos} to {to_pos} was be {distance}, but should be {expected_distance}"
