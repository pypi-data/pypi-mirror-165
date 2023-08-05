
from dataclasses import dataclass


@dataclass
class ChessPiece:
    name: str = ''
    value: int = 0
    letter: str = ''
    symbol: str = ''

@dataclass
class King(ChessPiece):
    name: str = 'King'
    value: int = 0
    letter: str = 'K'
    symbol: str = '\u2654'

@dataclass
class Queen(ChessPiece):
    name: str = 'Queen'
    value: int = 9
    letter: str = 'Q'
    symbol: str = '\u2655'

@dataclass
class Rook(ChessPiece):
    name: str = 'Rook'
    value: int = 5
    letter: str = 'R'
    symbol: str = '\u2656'

@dataclass
class Bishop(ChessPiece):
    name: str = 'Bishop'
    value: int = 3
    letter: str = 'B'
    symbol: str = '\u2657'

@dataclass
class Knight(ChessPiece):
    name: str = 'Knight'
    value: int = 3
    letter: str = 'N'
    symbol: str = '\u2658'

@dataclass
class Pawn(ChessPiece):
    name: str = 'Pawn'
    value: int = 1
    letter: str = 'P'
    symbol: str = '\u2659'

