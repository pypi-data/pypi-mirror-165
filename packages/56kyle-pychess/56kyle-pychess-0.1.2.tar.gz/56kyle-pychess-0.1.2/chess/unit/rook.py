from typing import Set

from chess.color import Color
from chess.path import Path, INFINITE_STEPS
from chess.offset import LINEAR
from chess.piece import Rook
from chess.unit import Unit


ROOK_PATHS: Set[Path] = {Path(offset=offset, max_steps=INFINITE_STEPS) for offset in LINEAR}


class WhiteRook(Unit, Rook):
    color: Color = Color.WHITE
    paths: Set[Path] = ROOK_PATHS


class BlackRook(Unit, Rook):
    color: Color = Color.BLACK
    paths: Set[Path] = ROOK_PATHS

