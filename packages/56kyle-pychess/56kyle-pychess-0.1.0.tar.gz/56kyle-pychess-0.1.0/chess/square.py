
from dataclasses import dataclass

from chess.offset import Offset


@dataclass(frozen=True)
class Square:
    row: int
    column: int

    def offset(self, offset: Offset) -> 'Square':
        return Square(self.row + offset.dy, self.column + offset.dx)

