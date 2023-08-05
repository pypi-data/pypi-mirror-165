
from chess.color import Color
from chess.move import Move
import chess.notation.base as base


class AlgebraicNotation(base.Notation):
    @classmethod
    def get_indexes_from_square(cls, square: str) -> (int, int):
        if square[0] not in 'abcdefgh':
            raise ValueError('Invalid column')
        if square[1] not in '12345678':
            raise ValueError('Invalid row')
        return ord(square[0]) - ord('a'), int(square[1]) - 1

