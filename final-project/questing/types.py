from typing import NamedTuple

class Position(NamedTuple):
    """A position is just a named tupled, so the x and y coordinates can be accessed by name (i.e. pos.x, pos.y)
    or by index (i.e. pos[0], pos[1]). It also provides a method to measure distances to other positions,
    the 'distance' method."""
    x: int
    y:int

    def distance(self, to: "Position") -> int:
        """Calculates the distance between two points, using the Manhattan distance. This means that the
        distance between (0, 0) and (1, 1) is 2, instead of sqrt(2), which would be the distance in a straight line."""
        return abs(self.x - to.x) + abs(self.y - to.y)
