
from dataclasses import dataclass


@dataclass(frozen=True)
class Offset:
    """An offset in a two dimensional numpy array"""
    dy: int = 0
    dx: int = 0

    def __add__(self, other):
        if isinstance(other, Offset):
            return Offset(self.dy + other.dy, self.dx + other.dx)
        else:
            return Offset(self.dy + int(other), self.dx + int(other))

    def __sub__(self, other):
        if isinstance(other, Offset):
            return Offset(self.dy - other.dy, self.dx - other.dx)
        else:
            return Offset(self.dy - int(other), self.dx - int(other))

    def __mul__(self, other):
        if isinstance(other, Offset):
            return Offset(self.dy * other.dy, self.dx * other.dx)
        else:
            return Offset(self.dy * int(other), self.dx * int(other))

    def is_linear(self) -> bool:
        return self.dy == 0 or self.dx == 0

    def is_diagonal(self) -> bool:
        return self.dy != 0 and self.dx != 0


UP = Offset(dy=-1, dx=0)
DOWN = Offset(dy=1, dx=0)
LEFT = Offset(dy=0, dx=-1)
RIGHT = Offset(dy=0, dx=1)

UP_LEFT = UP + LEFT
UP_RIGHT = UP + RIGHT
DOWN_LEFT = DOWN + LEFT
DOWN_RIGHT = DOWN + RIGHT

VERTICAL = {UP, DOWN}
HORIZONTAL = {LEFT, RIGHT}
LINEAR = VERTICAL | HORIZONTAL
DIAGONAL = {UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT}
ALL = LINEAR | DIAGONAL



