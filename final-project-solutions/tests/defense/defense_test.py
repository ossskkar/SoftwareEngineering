import pytest

from questing.defense import Defense

@pytest.fixture(params=[1, 3, 5, 10])
def health(request):
    return request.param

def test_health_attribute():
    defense = Defense(health=100)

    assert hasattr(defense, "health"), f"Defense should have a health attribute"

def test_health_is_set(health):
    defense = Defense(health=health)

    assert defense.health == health, f"Health should be {health}, but it was {defense.health}"

def test_take_damage(capsys):
    defense = Defense(health=20)
    expected_msgs = [
        f"I took 5 damage, I have 15 health points left",
        f"I took 12 damage, I have 3 health points left",
        f"I took 8 damage, and I've been destroyed!",
    ]

    res1 = defense.take_damage(5)
    res2 = defense.take_damage(12)
    res3 = defense.take_damage(8)
    out, _ = capsys.readouterr()

    assert res1 == False, f"take_damage should return False when the target is not destroyed"
    assert res2 == False, f"take_damage should return False when the target is not destroyed"
    assert res3 == True, f"take_damage should return True when the target is destroyed"
    for msg in expected_msgs:
        assert msg in out

def test_is_alive():
    defense = Defense(health=10)

    assert defense.is_alive == True, f"is_alive should be True when health > 0"

    defense.take_damage(10)

    assert defense.is_alive == False, f"is_alive should return False when there's no health left"

def test_heal(capsys):
    defense = Defense(health=20)
    defense.take_damage(19)
    expected_msgs = [
        f"Restoring 10 points of health",
        f"Health after healing: 11 (before: 1)",
    ]

    assert defense.health == 1, f"Initial health should be 1"
    defense.heal(10)
    assert defense.health == 11, f"Health after healing should be 11"
    out, _ = capsys.readouterr()

    for msg in expected_msgs:
        assert msg in out

def test_heal_above_max_health(capsys):
    defense = Defense(health=20)
    defense.take_damage(19)
    expected_msgs = [
        f"Restoring 100 points of health",
        f"Health after healing: 20 (before: 1)",
    ]

    assert defense.health == 1, f"Initial health should be 1"
    defense.heal(100)
    assert defense.health == 20, f"Health after healing should be 20"
    out, _ = capsys.readouterr()

    for msg in expected_msgs:
        assert msg in out

def test_heal_to_max_health(capsys):
    defense = Defense(health=20)
    defense.take_damage(19)
    expected_msgs = [
        f"Restoring to full health (20 points)",
    ]

    assert defense.health == 1, f"Initial health should be 1"
    defense.heal()
    assert defense.health == 20, f"Health after healing should be 20"
    out, _ = capsys.readouterr()

    for msg in expected_msgs:
        assert msg in out
