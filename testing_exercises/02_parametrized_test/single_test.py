from typing import Union

Number = Union[int, float]
class Calculator:
    def sum(self, x: Number, y: Number) -> Number:
        return x + y

import pytest

def test_sums():
    sum_data = [
        #x, y, expected_result
        (1, 2, 3),
        (3, 0, 3),
        (-5, 2, -3),
        (-5, -2, -7),
    ]

    for x, y, expected_result in sum_data:
        result = Calculator().sum(x, y)

        assert result == expected_result, \
            f"{x} + {y} is {expected_result}, but the actual result was {result}"
