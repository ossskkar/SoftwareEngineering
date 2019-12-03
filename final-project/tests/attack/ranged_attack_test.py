from unittest import mock
import math

import pytest

from questing.attack import RangedAttack
from questing import Position


@pytest.fixture(params=[0, 1, 2, 5])
def power(request):
    return request.param

@pytest.fixture(params=[2, 3, 5])
def attack_range(request):
    return request.param


def test_power_attribute():
    attack = RangedAttack(power=1, attack_range=2)

    assert hasattr(attack, "power"), f"RangedAttack should have a power attribute"

def test_power_is_set(power):
    attack = RangedAttack(power=power, attack_range=2)

    assert attack.power == power, f"Power should be {power}, but it was {attack.power}"

def test_attack_range_attribute():
    attack = RangedAttack(power=1, attack_range=2)

    assert hasattr(attack, "attack_range"), f"RangedAttack should have an attack_range attribute"

def test_attack_range_is_set(attack_range):
    attack = RangedAttack(power=1, attack_range=attack_range)

    assert attack.attack_range == attack_range, f"Attack range should be {attack_range}, but it was {attack.attack_range}"

def test_attack_out_of_reach(capsys, attack_range):
    attacker = RangedAttack(power=1, attack_range=attack_range)
    from_pos = mock.MagicMock()
    target_pos = mock.MagicMock()
    distance = attack_range + 1
    from_pos.distance.return_value = distance
    msg = "Target is out of reach, can't attack!"

    attacker.position = from_pos
    target = mock.MagicMock()
    target.position = target_pos

    result = attacker.attack(target=target)
    out, _ = capsys.readouterr()

    assert result == False, f"Ranged attack with range of {attack_range} to a distance of {distance} should return False"
    assert msg.lower() in out.lower()
    from_pos.distance.assert_called_once_with(target_pos)

def test_attack_target_reachable(capsys):
    power = 2
    attack_range = 3
    attacker = RangedAttack(power=power, attack_range=attack_range)
    from_pos = mock.MagicMock()
    target_pos = mock.MagicMock()
    distance = attack_range
    from_pos.distance.return_value = distance

    attacker.position = from_pos
    target = mock.MagicMock()
    target.position = target_pos
    target.name = "Some Enemy"
    target.take_damage.return_value = True

    msgs = [
        f"Attacking {target.name} with power {power}",
    ]

    result = attacker.attack(target=target)
    out, _ = capsys.readouterr()

    assert result == True, f"RangedAttack should return the result of take_damage"
    for msg in msgs:
        assert msg.lower() in out.lower()
    from_pos.distance.assert_called_once_with(target_pos)
    target.take_damage.assert_called_once_with(power)

def test_attack_melee_range_uses_half_power(capsys):
    power = 2
    expected_power = math.ceil(power/2)
    attack_range = 3
    attacker = RangedAttack(power=power, attack_range=attack_range)
    from_pos = mock.MagicMock()
    target_pos = mock.MagicMock()
    distance = 1
    from_pos.distance.return_value = distance

    attacker.position = from_pos
    target = mock.MagicMock()
    target.position = target_pos
    target.name = "Some Enemy"
    target.take_damage.return_value = True

    msgs = [
        "Target is too close, will attack with half power",
        f"Attacking {target.name} with power {expected_power}",
    ]

    result = attacker.attack(target=target)
    out, _ = capsys.readouterr()

    assert result == True, f"RangedAttack should return the result of take_damage"
    for msg in msgs:
        assert msg.lower() in out.lower()

    from_pos.distance.assert_called_once_with(target_pos)
    target.take_damage.assert_called_once_with(expected_power)


