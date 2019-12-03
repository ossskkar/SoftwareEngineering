from typing import Union

Number = Union[int, float]
class Calculator:
    def sum(self, x: Number, y: Number) -> Number:
        return x + y

import pytest

SUM_FIXTURES = [
    (1, 2, 3),
    (1, 5, 6),
    (1, 4, 6),
    (-5, 4, -1),
]

@pytest.mark.parametrize("x,y,expected_result", SUM_FIXTURES)
def test_sum(x, y, expected_result):
    result = Calculator().sum(x, y)

    assert result == expected_result, \
        f"{x} + {y} is {expected_result}, but the actual result was {result}"
