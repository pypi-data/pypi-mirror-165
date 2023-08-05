from chess.color import Color
from chess.move import Move
from chess.notation import AlgebraicNotation


class FIDE(AlgebraicNotation):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


