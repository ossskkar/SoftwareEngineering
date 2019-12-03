import pytest

from unittest import mock

from questing import Army, Archer, Swordsman, Apprentice, Position, Unit


@pytest.fixture
def army_units():
    unit1 = Archer.create(level=2)
    unit2 = Swordsman.create(level=3)
    unit3 = Apprentice.create(level=1)

    return [unit1, unit2, unit3]

@pytest.fixture
def army(army_units):
    return Army(units=army_units)

def test_position_is_set_on_all_units(army_units):
    pos = Position(3, 5)
    army = Army(units=army_units, position=pos)

    assert army.position == pos, f"Army position should be {pos}, but it was {army.position}"

    for u in army_units:
        assert u.position == pos, f"Position for unit {u.name} should be {pos}, but it was {u.position}"

def test_army_health(army, army_units):
    expected_health = sum(map(lambda u: u.health, army_units))

    assert army.health == expected_health, f"Army health should be the sum of the health of all units"

def test_army_speed(army, army_units):
    expected_speed = min(map(lambda u: u.speed, army_units))

    assert army.speed == expected_speed, f"Army speed should be the lowest speed among units in the army"

def test_army_level(army, army_units):
    expected_level = sum(map(lambda u: u.level, army_units))

    assert army.level == expected_level, f"Army level should be the sum of levels of all units in the army"

def test_add_unit_to_army(army, army_units):
    new_unit = Archer.create(level=5)
    initial_health = sum(map(lambda u: u.health, army_units))
    initial_speed = min(map(lambda u: u.speed, army_units))
    initial_level = sum(map(lambda u: u.level, army_units))

    expected_health = initial_health + new_unit.health
    expected_speed = min(initial_speed, new_unit.speed)
    expected_level = initial_level + new_unit.level

    army += new_unit

    assert army.health == expected_health, f"New army health should be {expected_health}, but was {army.health}"
    assert army.speed == expected_speed, f"New army speed should be {expected_speed}, but was {army.speed}"
    assert army.level == expected_level, f"New army level should be {expected_level}, but was {army.level}"

def test_attack_when_target_survives():
    unit1 = mock.MagicMock(spec=Unit)
    unit2 = mock.MagicMock(spec=Unit)

    target = mock.MagicMock(spec=Unit)
    target.is_alive = True

    army = Army(units=[unit1, unit2])

    result = army.attack(target)

    assert result == False, "Army attack should return False if target was not destroyed"
    unit1.attack.assert_called_once_with(target)
    unit2.attack.assert_called_once_with(target)

def test_attack_when_target_is_killed():
    unit1 = mock.MagicMock(spec=Unit)
    unit2 = mock.MagicMock(spec=Unit)

    target = mock.MagicMock(spec=Unit)
    target.is_alive = False

    army = Army(units=[unit1, unit2])

    result = army.attack(target)

    assert result == True, "Army attack should return True if target was destroyed"
    unit1.attack.assert_called_once_with(target)
    unit2.attack.assert_not_called()

def test_take_damage_with_no_unit_destroyed(army, army_units):
    initial_health = army.units[0].health

    result = army.take_damage(1)

    assert result == False, "take_damage should return False when the army is still alive"
    assert army.units[0].health == initial_health - 1, "damage should go to the first unit in the army"

def test_take_damage_with_unit_destroyed(army, army_units):
    # Destroy all units in the army, one by one
    for u in army_units:
        while u.is_alive:
            result = army.take_damage(u.health)

    assert result == True, "take_damage should return True when the army has been destroyed"
    assert len(army.units) == 0, "The army should have no units left"
    assert army.is_alive == False, "An army with no units shouldn't be alive"

def test_army_short_text(army):
    assert army.short_text == "R", f"Army short text should be 'R', but it was '{army.short_text}'"