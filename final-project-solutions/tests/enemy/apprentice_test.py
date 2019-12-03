import pytest

from questing import Apprentice
from questing.attack import MagicAttack
from questing.defense import Barrier

def test_base_health():
    assert Apprentice.BASE_HEALTH == 4, "Apprentice should have a base health of 4"

def test_base_range():
    assert Apprentice.BASE_RANGE == 2, "Apprentice should have a base range of 2"

def test_base_power():
    assert Apprentice.BASE_POWER == 3, "Apprentice should have a base power of 3"

def test_base_speed():
    assert Apprentice.BASE_SPEED == 1, "Apprentice should have a base speed of 1"

def test_base_armor():
    assert Apprentice.BASE_ARMOR == 1, "Apprentice should have a base armor of 1"

def test_apprentice_short_text():
    apprentice = Apprentice.create(level=1)

    assert apprentice.short_text == "M", "Short text for the Apprentice class should be 'M'"

def test_apprentice_has_magic_attack():
    apprentice = Apprentice.create(level=1)

    assert isinstance(apprentice, MagicAttack), "Apprentice should have MagicAttack"

def test_apprentice_has_barrier():
    apprentice = Apprentice.create(level=1)

    assert isinstance(apprentice, Barrier), "Apprentice should have a Barrier"

def test_create_increases_num_units():
    Apprentice.NUM_UNITS = 0
    _ = Apprentice.create(level=1)

    assert Apprentice.NUM_UNITS == 1, "Apprentice.NUM_UNITS should increase by 1 after calling create"

def test_create_sets_name_based_on_num_units():
    # This is the current number of units
    Apprentice.NUM_UNITS = 3
    apprentice = Apprentice.create(level=1)

    assert apprentice.name == "Apprentice 4", "Name of the new unit should use Apprentice.NUM_UNITS"

def test_string_representation_has_level():
    apprentice = Apprentice.create(level=3)

    expected_str = f"M(3)"

    assert str(apprentice) == expected_str, "Expected level 3 Apprentice to be represented as 'M(3)'"
