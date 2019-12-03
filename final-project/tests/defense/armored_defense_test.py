import pytest

from questing.defense import ArmoredDefense


@pytest.fixture(params=[1, 3, 5])
def armor(request):
    return request.param

def test_armor_attribute():
    defense = ArmoredDefense(health=10, armor=1)

    assert hasattr(defense, "armor"), f"Defense should have an armor attribute"

def test_armor_is_set(armor):
    defense = ArmoredDefense(health=10, armor=armor)

    assert defense.armor == armor, f"Armor should be {armor}, but it was {defense.armor}"

def test_take_damage_absorbs_damage(capsys):
    defense = ArmoredDefense(health=10, armor=2)

    defense.take_damage(5)
    out, _ = capsys.readouterr()

    expected_msgs = [
        f"I took 3 damage, I have 7 health points left",
        f"Armor absorved 2 damage, taking 3 damage instead of 5",
    ]

    assert defense.health == 7, \
        f"With health=10 and armor=2, defense should have 7 health points left after taking 5 points of damage"

    for msg in expected_msgs:
        assert msg in out

def test_take_damage_with_armor_greater_than_damage(capsys):
    defense = ArmoredDefense(health=10, armor=10)

    defense.take_damage(5)
    out, _ = capsys.readouterr()

    expected_msgs = [
        f"I took 0 damage, I have 10 health points left",
        f"Armor absorved 5 damage, taking 0 damage instead of 5",
    ]

    assert defense.health == 10, \
        f"With health=10 and armor=2, defense should have 7 health points left after taking 5 points of damage"

    for msg in expected_msgs:
        assert msg in out