import pytest
from unittest import mock

from questing import Enemy, Archer, Swordsman, Apprentice

def test_create_random_enemy():
    enemy_class_mock = mock.MagicMock()
    enemy_mock = mock.MagicMock(spec=Enemy)
    enemy_class_mock.create.return_value = enemy_mock
    expected_classes = [Archer, Swordsman, Apprentice]
    with mock.patch("numpy.random.choice", return_value=enemy_class_mock) as np_mock:
        enemy = Enemy.random_enemy(level=3)

    np_mock.assert_called_once_with(expected_classes)
    enemy_class_mock.create.assert_called_once_with(level=3)
    assert enemy == enemy_mock, "The result of [EnemyClass].create have been returned"

