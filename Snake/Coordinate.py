import random
from typing import NamedTuple


class Coordinate(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Coordinate") -> "Coordinate":
        return Coordinate(self.x - other.x, self.y - other.y)

    @classmethod
    def random_coord(cls, max_x: int, max_y: int,min_x:int=0,min_y:int=0) -> "Coordinate":
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        return cls(x, y)