from typing import List

import numpy as np

from chess.color import Color
from chess.unit import (
    Unit,
    BlackKing,
    BlackQueen,
    BlackRook,
    BlackBishop,
    BlackKnight,
    BlackPawn,
    WhiteKing,
    WhiteQueen,
    WhiteRook,
    WhiteBishop,
    WhiteKnight,
    WhitePawn,
)
from chess.square import Square


standard_black_pieces = [
    BlackRook, BlackKnight, BlackBishop, BlackQueen, BlackKing, BlackBishop, BlackKnight, BlackRook,
    BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn,

]

standard_white_pieces = [
    WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn,
    WhiteRook, WhiteKnight, WhiteBishop, WhiteQueen, WhiteKing, WhiteBishop, WhiteKnight, WhiteRook,
]

standard_pieces = [*standard_black_pieces, *standard_white_pieces]


standard_board_array = np.array(
    [[BlackRook, BlackKnight, BlackBishop, BlackQueen, BlackKing, BlackBishop, BlackKnight, BlackRook],
     [BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn, BlackPawn],
     [None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None],
     [None, None, None, None, None, None, None, None],
     [WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn, WhitePawn],
     [WhiteRook, WhiteKnight, WhiteBishop, WhiteQueen, WhiteKing, WhiteBishop, WhiteKnight, WhiteRook]]
)
class ChessBoard:
    def __init__(self, array: np.ndarray = standard_board_array, *args, **kwargs):
        self._array: np.ndarray = array

    def __eq__(self, other):
        if isinstance(other, ChessBoard):
            return np.array_equal(self._array, other._array)
        elif isinstance(other, np.ndarray):
            return np.array_equal(self._array, other)
        else:
            return False

    def get(self, square: Square) -> Unit | None:
        return self._array[square.row][square.column]

    def set(self, square: Square, unit: Unit | None):
        self._array[square.row][square.column] = unit

    def get_height(self) -> int:
        return self._array.shape[0]

    def get_width(self) -> int:
        return self._array.shape[1]

    def get_max_y_index(self) -> int:
        return self.get_height() - 1

    def get_max_x_index(self) -> int:
        return self.get_width() - 1

    def get_units(self) -> List[Unit]:
        units = []
        for square in self._array.flatten():
            if square is not None:
                units.append(square)
        return units

    def get_absolute_max_path_steps(self) -> int:
        return max(self.get_height(), self.get_width())

    def is_valid_square(self, square: Square) -> bool:
        return 0 <= square.row < self.get_height() and 0 <= square.column < self.get_width()


