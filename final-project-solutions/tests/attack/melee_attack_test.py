from unittest import mock

import pytest

from questing.attack import MeleeAttack
from questing import Position


@pytest.fixture(params=[0, 1, 2, 5])
def power(request):
    return request.param

def test_power_attribute():
    attack = MeleeAttack(power=1)

    assert hasattr(attack, "power"), f"MeleeAttack should have a power attribute"

def test_power_is_set(power):
    attack = MeleeAttack(power=power)

    assert attack.power == power, f"Power should be {power}, but it was {attack.power}"

def test_attack_out_of_reach(capsys):
    attacker = MeleeAttack(power=1)
    from_pos = mock.MagicMock()
    target_pos = mock.MagicMock()
    distance = 5
    from_pos.distance.return_value = distance
    msg = "Target is out of reach, can't attack!"

    attacker.position = from_pos
    target = mock.MagicMock()
    target.position = target_pos

    result = attacker.attack(target=target)
    out, _ = capsys.readouterr()

    assert result == False, f"Melee attacking to a distance of 5 should return False"
    assert msg.lower() in out.lower()
    from_pos.distance.assert_called_once_with(target_pos)

def test_attack_target_reachable(capsys):
    power = 1
    attacker = MeleeAttack(power=power)
    from_pos = mock.MagicMock()
    target_pos = mock.MagicMock()
    distance = 1
    from_pos.distance.return_value = distance

    attacker.position = from_pos
    target = mock.MagicMock()
    target.position = target_pos
    target.name = "Some Enemy"
    target.take_damage.return_value = True

    msg = f"Attacking {target.name}!"

    result = attacker.attack(target=target)
    out, _ = capsys.readouterr()

    assert result == True, f"Melee attacking at a distance of 1 should return the result of take_damage"
    assert msg.lower() in out.lower()
    from_pos.distance.assert_called_once_with(target_pos)
    target.take_damage.assert_called_once_with(power)



