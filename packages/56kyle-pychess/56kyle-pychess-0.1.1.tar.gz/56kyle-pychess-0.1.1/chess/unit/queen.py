

from typing import Set

from chess.color import Color
from chess.path import Path, INFINITE_STEPS
from chess.offset import LINEAR, DIAGONAL
from chess.piece import Queen
from chess.unit import Unit


QUEEN_PATHS: Set[Path] = {Path(offset=offset, max_steps=INFINITE_STEPS) for offset in LINEAR | DIAGONAL}


class WhiteQueen(Unit, Queen):
    color: Color = Color.WHITE
    paths: Set[Path] = QUEEN_PATHS


class BlackQueen(Unit, Queen):
    color: Color = Color.BLACK
    paths: Set[Path] = QUEEN_PATHS

