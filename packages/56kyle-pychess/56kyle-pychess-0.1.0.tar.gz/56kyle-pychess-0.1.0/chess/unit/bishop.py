from typing import Set

from chess.color import Color
from chess.path import Path, INFINITE_STEPS
from chess.offset import DIAGONAL
from chess.piece import Bishop
from chess.unit import Unit


BISHOP_PATHS: Set[Path] = {Path(offset=offset, max_steps=INFINITE_STEPS) for offset in DIAGONAL}

class WhiteBishop(Unit, Bishop):
    color: Color = Color.WHITE
    paths: Set[Path] = BISHOP_PATHS


class BlackBishop(Unit, Bishop):
    color: Color = Color.BLACK
    paths: Set[Path] = BISHOP_PATHS

