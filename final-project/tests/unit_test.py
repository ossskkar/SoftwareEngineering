import pytest

from questing import Unit, Position

@pytest.mark.skip
class NonAbstractUnit(Unit):
    def attack(self, target: "Unit") -> bool:
        return True

    def take_damage(self, damage: int) -> bool:
        return False

    @property
    def short_text(self):
        return "U"

@pytest.fixture
def unit():
    return NonAbstractUnit(speed=1, position=Position(0, 0))


def test_move_with_0_speed(capsys, unit):
    unit.speed = 0
    expected_msg = "My speed is 0, I can't move!"

    result = unit.move(destination=Position(1, 1))
    out, _ = capsys.readouterr()

    assert result == False, "unit.move should be False if the unit can't move"
    assert expected_msg in out

def test_move_when_in_range(capsys, unit):
    destination = Position(0, 1)
    expected_msg = f"Moving to new position ({destination})"

    result = unit.move(destination)
    out, _ = capsys.readouterr()

    assert result == True, "Result should be true when unit can move to the position"
    assert unit.position == destination, f"New position after moving should be {destination}"
    assert expected_msg in out

def test_move_when_in_not_range(capsys, unit):
    destination = Position(10, 0)
    expected_msg = f"Target position {destination} is at a distance of 10 and my speed is 1, I can't reach it!"

    result = unit.move(destination)
    out, _ = capsys.readouterr()

    assert result == False, "Result should be False when unit can't move to the position"
    assert unit.position == Position(0, 0), f"Position should still be the same after a failed attempt to move"
    assert expected_msg in out

def test_unit_to_str(unit):
    assert str(unit) == "U"
