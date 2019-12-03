import pytest

from questing.defense import Barrier


@pytest.fixture(params=[1, 3, 5])
def armor(request):
    return request.param

def test_armor_attribute():
    defense = Barrier(health=10, armor=1)

    assert hasattr(defense, "armor"), f"Defense should have an armor attribute"

def test_armor_is_set(armor):
    defense = Barrier(health=10, armor=armor)

    assert defense.armor == armor, f"Armor should be {armor}, but it was {defense.armor}"

def test_take_damage_absorbs_damage_and_reduces_armor(capsys):
    defense = Barrier(health=10, armor=10)

    defense.take_damage(2)
    out, _ = capsys.readouterr()

    expected_msgs = [
        f"I took 0 damage, I have 10 health points left",
        f"Armor absorved 2 damage, taking 0 damage instead of 2",
    ]

    assert defense.health == 10, \
        f"With health=10 and armor=10, barrier defense should have 10 health points left after taking 2 points of damage"
    assert defense.armor == 8, \
        f"With health=10 and armor=10, barrier defense should have 8 armor points left after taking 2 points of damage"

    for msg in expected_msgs:
        assert msg in out

def test_barrier_breaks(capsys):
    defense = Barrier(health=10, armor=5)
    expected_msgs = [
        f"I took 1 damage, I have 9 health points left",
        f"Armor absorved 5 damage, taking 1 damage instead of 6",
        "My armor has been broken!",
    ]

    defense.take_damage(6)
    out, _ = capsys.readouterr()

    assert defense.health == 9, \
        f"With health=10 and armor=5, barrier defense should have 9 health points left after taking 6 points of damage"
    assert defense.armor == 0, \
        f"With health=10 and armor=5, barrier defense should have 0 armor points left after taking 6 points of damage"

    for msg in expected_msgs:
        assert msg in out

def test_no_damage_is_absorbed_after_barrier_breaks(capsys):
    defense = Barrier(health=10, armor=5)
    expected_msgs = [
        f"I took 0 damage, I have 10 health points left",
        f"Armor absorved 5 damage, taking 0 damage instead of 5",
        "My armor has been broken!",
        f"I took 4 damage, I have 6 health points left",
    ]

    defense.take_damage(5)

    assert defense.health == 10, \
        f"With health=10 and armor=5, barrier defense should have 10 health points left after taking 5 points of damage"
    assert defense.armor == 0, \
        f"With health=10 and armor=5, barrier defense should have 0 armor points left after taking 5 points of damage"

    defense.take_damage(4)
    out, _ = capsys.readouterr()

    for msg in expected_msgs:
        assert msg in out