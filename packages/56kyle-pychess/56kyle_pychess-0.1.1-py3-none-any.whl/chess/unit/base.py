

from abc import ABC, abstractmethod

from typing import Set

from chess.color import Color
from chess.piece import ChessPiece
from chess.path import Path


class Unit(ChessPiece, ABC):
    color: Color
    paths: Set[Path]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_moved = False


