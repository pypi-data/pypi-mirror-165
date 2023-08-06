
from abc import ABC, abstractmethod
from chess.move import Move


class Notation:
    def __init__(self, move: Move, *args, **kwargs):
        self.move: Move = move

    def __str__(self):
        return self._get_notation_string()

    @classmethod
    def get_move_from_string(cls, notation: str):
        raise NotImplementedError()

    def _get_notation_string(self):
        raise NotImplementedError()



