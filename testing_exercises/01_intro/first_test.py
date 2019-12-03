def add_two(number: int) -> int:
    """This function just adds 2 to any number it receives"""
    return number + 2

def test_add_two():
    number = 1
    expected_result = 3

    result = add_two(number)

    assert result == expected_result, \
        f"The result of adding 2 to {number} should be {expected_result}, but it was {result}!"

def test_add_two_to_3():
    number = 3
    expected_result = 5

    result = add_two(number)

    assert result == expected_result, \
        f"The result of adding 2 to {number} should be {expected_result}, but it was {result}!"

def test_add_two_to_minus_6():
    number = -6
    expected_result = -4

    result = add_two(number)

    assert result == expected_result, \
        f"The result of adding 2 to {number} should be {expected_result}, but it was {result}!"
