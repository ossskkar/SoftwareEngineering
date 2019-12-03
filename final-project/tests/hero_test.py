import pytest

from questing import Warrior, Rogue, Mage

@pytest.fixture(params=[Warrior, Rogue, Mage])
def hero_class(request):
    return request.param

def test_short_text(hero_class):
    hero = hero_class(name="Test Hero")

    assert hero.short_text == "H", "Short text for hero should be 'H'"

def test_hero_name(hero_class):
    name = "Test Hero"
    hero = hero_class(name=name)
    expected_name = f"{name} - {hero_class.__name__}"

    assert hero.name == expected_name, f"Hero name should be {expected_name}, but was {hero.name}"

def test_warrior_stats():
    hero = Warrior(name="Test")

    assert hero.power == 4, "Warrior power should be 4"
    assert hero.armor == 1, "Warrior armor should be 1"
    assert hero.speed == 1, "Warrior speed should be 1"
    assert hero.health == 10, "Warrior health should be 10"

def test_rogue_stats():
    hero = Rogue(name="Test")

    assert hero.power == 3, "Rogue power should be 3"
    assert hero.attack_range == 3, "Rogue attack_range should be 3"
    assert hero.speed == 2, "Rogue speed should be 2"
    assert hero.health == 9, "Rogue health should be 9"

def test_mage_stats():
    hero = Mage(name="Test")

    assert hero.power == 3, "Mage power should be 3"
    assert hero.armor == 2, "Mage armor(barrier) should be 2"
    assert hero.attack_range == 2, "Mage attack_range should be 2"
    assert hero.speed == 1, "Mage speed should be 1"
    assert hero.health == 8, "Mage health should be 8"
