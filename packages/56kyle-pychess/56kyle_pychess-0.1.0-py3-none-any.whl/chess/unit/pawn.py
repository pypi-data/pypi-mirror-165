
from typing import Set

from chess.color import Color
from chess.path import Path, AllowedMovementTypes
from chess.offset import UP, DOWN, UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT
from chess.piece import Pawn
from chess.unit import Unit


WHITE_PAWN_FIRST_PATH = Path(offset=UP * 2, max_steps=1, allowed_path_types=AllowedMovementTypes.MOVE_ONLY)
WHITE_PAWN_STANDARD_PATH = Path(offset=UP, max_steps=1, allowed_path_types=AllowedMovementTypes.MOVE_ONLY)
WHITE_PAWN_CAPTURE_PATHS = {
    Path(
        offset=offset,
        max_steps=1,
        allowed_path_types=AllowedMovementTypes.CAPTURE_ONLY,
    ) for offset in {UP_RIGHT, UP_LEFT}
}
WHITE_PAWN_PATHS = {WHITE_PAWN_FIRST_PATH, WHITE_PAWN_STANDARD_PATH} | WHITE_PAWN_CAPTURE_PATHS

BLACK_PAWN_FIRST_PATH = Path(offset=DOWN * 2, max_steps=1, allowed_path_types=AllowedMovementTypes.MOVE_ONLY)
BLACK_PAWN_STANDARD_PATH = Path(offset=DOWN, max_steps=1, allowed_path_types=AllowedMovementTypes.MOVE_ONLY)
BLACK_PAWN_CAPTURE_PATHS = {
    Path(
        offset=offset,
        max_steps=1,
        allowed_path_types=AllowedMovementTypes.CAPTURE_ONLY
    ) for offset in {DOWN_RIGHT, DOWN_LEFT}
}
BLACK_PAWN_PATHS = {BLACK_PAWN_FIRST_PATH, BLACK_PAWN_STANDARD_PATH} | BLACK_PAWN_CAPTURE_PATHS


class WhitePawn(Unit, Pawn):
    color: Color = Color.WHITE
    paths: Set[Path] = WHITE_PAWN_PATHS


class BlackPawn(Unit, Pawn):
    color: Color = Color.BLACK
    paths: Set[Path] = BLACK_PAWN_PATHS

