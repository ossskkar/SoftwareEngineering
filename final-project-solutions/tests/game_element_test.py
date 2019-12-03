import pytest

from questing import GameElement, Wall, ExitPortal, Position

# The GameElement class is abstract, so we test indirectly via a child class

def test_position_attribute():
    element = Wall()

    assert hasattr(element, "position"), f"GameElement should have a position attribute"
    assert element.position is None, "If not provided, the element's position should be None"

def test_position_is_set():
    pos = Position(1, 1)
    element = Wall(position=pos)

    assert element.position == pos, f"GameElement should have position {pos}, but it was {element.position}"

def test_wall_short_text():
    element = Wall()

    assert element.short_text == "W", f"Short text for walls should be 'W', but it was '{element.short_text}'"

def test_exit_portal_short_text():
    element = ExitPortal()

    assert element.short_text == "EXIT", f"Short text for exit portal should be 'EXIT', but it was '{element.short_text}'"
