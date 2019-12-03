import pytest

from questing import Swordsman
from questing.attack import MeleeAttack
from questing.defense import ArmoredDefense

def test_base_health():
    assert Swordsman.BASE_HEALTH == 4, "Swordsman should have a base health of 4"

def test_base_armor():
    assert Swordsman.BASE_ARMOR == 1, "Swordsman should have a base armor of 1"

def test_base_power():
    assert Swordsman.BASE_POWER == 3, "Swordsman should have a base power of 3"

def test_base_speed():
    assert Swordsman.BASE_SPEED == 1, "Swordsman should have a base speed of 1"

def test_swordsman_short_text():
    swordsman = Swordsman.create(level=1)

    assert swordsman.short_text == "S", "Short text for the Swordsman class should be 'S'"

def test_swordsman_has_melee_attack():
    swordsman = Swordsman.create(level=1)

    assert isinstance(swordsman, MeleeAttack), "Swordsman should have MeleeAttack"

def test_swordsman_has_armored_defense():
    swordsman = Swordsman.create(level=1)

    assert isinstance(swordsman, ArmoredDefense), "Swordsman should have ArmoredDefense"

def test_create_increases_num_units():
    Swordsman.NUM_UNITS = 0
    _ = Swordsman.create(level=1)

    assert Swordsman.NUM_UNITS == 1, "Swordsman.NUM_UNITS should increase by 1 after calling create"

def test_create_sets_name_based_on_num_units():
    # This is the current number of units
    Swordsman.NUM_UNITS = 3
    swordsman = Swordsman.create(level=1)

    assert swordsman.name == "Swordsman 4", "Name of the new unit should use Swordsman.NUM_UNITS"

def test_string_representation_has_level():
    swordsman = Swordsman.create(level=3)

    expected_str = f"S(3)"

    assert str(swordsman) == expected_str, "Expected level 3 Swordsman to be represented as 'S(3)'"
