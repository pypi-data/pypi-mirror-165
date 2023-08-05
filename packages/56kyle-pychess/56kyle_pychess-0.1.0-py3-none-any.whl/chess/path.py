
from dataclasses import dataclass
from enum import Enum

from chess.offset import Offset


INFINITE_STEPS = 0


class AllowedMovementTypes(Enum):
    MOVE_ONLY = 1
    CAPTURE_ONLY = 2
    BOTH = 3


@dataclass(frozen=True)
class Path:
    offset: Offset = Offset(dy=0, dx=0)
    max_steps: int = INFINITE_STEPS
    allowed_path_types: AllowedMovementTypes = AllowedMovementTypes.BOTH

    def with_limited_max_steps(self, max_steps: int) -> 'Path':
        new_max_steps: int = min(self.max_steps, max_steps) if self.max_steps != INFINITE_STEPS else max_steps
        return Path(self.offset, new_max_steps, self.allowed_path_types)

    def limit_to_shape(self, height: int, width: int) -> 'Path':
        return Path(self.offset, self._get_shape_limited_steps(height, width), self.allowed_path_types)

    def _get_shape_limited_steps(self, height: int, width: int) -> int:
        height_limited_steps: int = self._get_height_limited_steps(height)
        width_limited_steps: int = self._get_width_limited_steps(width)
        return min(height_limited_steps, width_limited_steps)

    def limit_to_height(self, height: int) -> 'Path':
        return Path(self.offset, self._get_height_limited_steps(height), self.allowed_path_types)

    def _get_height_limited_steps(self, height: int) -> int:
        height_limited_steps: int = height // abs(self.offset.dy)
        if self.max_steps == INFINITE_STEPS:
            return height_limited_steps
        return min(self.max_steps, height_limited_steps)

    def limit_to_width(self, width: int) -> 'Path':
        return Path(self.offset, self._get_width_limited_steps(width), self.allowed_path_types)

    def _get_width_limited_steps(self, width: int) -> int:
        width_limited_steps: int = width // abs(self.offset.dx)
        if self.max_steps == INFINITE_STEPS:
            return width_limited_steps
        return min(self.max_steps, width_limited_steps)


