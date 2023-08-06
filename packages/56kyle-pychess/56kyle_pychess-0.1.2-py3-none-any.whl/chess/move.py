
from dataclasses import dataclass
import chess.piece

from chess.square import Square


@dataclass
class Move:
    piece: chess.piece.ChessPiece
    from_square: Square
    to_square: Square
    captured_piece: chess.piece.ChessPiece = None
    promotion: chess.piece.ChessPiece = None
    check: bool = False


