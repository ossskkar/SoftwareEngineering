import pytest

from questing import Archer
from questing.attack import RangedAttack
from questing.defense import Defense

def test_base_health():
    assert Archer.BASE_HEALTH == 3, "Archer should have a base health of 3"

def test_base_range():
    assert Archer.BASE_RANGE == 2, "Archer should have a base range of 2"

def test_base_power():
    assert Archer.BASE_POWER == 3, "Archer should have a base power of 3"

def test_base_speed():
    assert Archer.BASE_SPEED == 1, "Archer should have a base speed of 1"

def test_archer_short_text():
    archer = Archer.create(level=1)

    assert archer.short_text == "A", "Short text for the archer class should be 'A'"

def test_archer_has_ranged_attack():
    archer = Archer.create(level=1)

    assert isinstance(archer, RangedAttack), "Archer should have RangedAttack"

def test_archer_has_defense():
    archer = Archer.create(level=1)

    assert isinstance(archer, Defense), "Archer should have Defense"

def test_create_increases_num_units():
    Archer.NUM_UNITS = 0
    _ = Archer.create(level=1)

    assert Archer.NUM_UNITS == 1, "Archer.NUM_UNITS should increase by 1 after calling create"

def test_create_sets_name_based_on_num_units():
    # This is the current number of units
    Archer.NUM_UNITS = 3
    archer = Archer.create(level=1)

    assert archer.name == "Archer 4", "Name of the new unit should use Archer.NUM_UNITS"

def test_string_representation_has_level():
    archer = Archer.create(level=3)

    expected_str = f"A(3)"

    assert str(archer) == expected_str, "Expected level 3 archer to be represented as 'A(3)'"
