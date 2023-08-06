
from typing import Set

from chess.color import Color
from chess.path import Path, AllowedMovementTypes
from chess.offset import RIGHT, LEFT, LINEAR, DIAGONAL
from chess.piece import King
from chess.unit import Unit


KING_SIDE_CASTLE_PATH = Path(offset=RIGHT * 2, max_steps=1, allowed_path_types=AllowedMovementTypes.MOVE_ONLY)
QUEEN_SIDE_CASTLE_PATH = Path(offset=LEFT * 3, max_steps=1, allowed_path_types=AllowedMovementTypes.MOVE_ONLY)
CASTLE_PATHS = {KING_SIDE_CASTLE_PATH, QUEEN_SIDE_CASTLE_PATH}

STANDARD_KING_PATHS = {Path(offset=offset, max_steps=1) for offset in LINEAR | DIAGONAL}
KING_PATHS = STANDARD_KING_PATHS | CASTLE_PATHS


class WhiteKing(Unit, King):
    color: Color = Color.WHITE
    paths: Set[Path] = KING_PATHS


class BlackKing(Unit, King):
    color: Color = Color.BLACK
    paths: Set[Path] = KING_PATHS

