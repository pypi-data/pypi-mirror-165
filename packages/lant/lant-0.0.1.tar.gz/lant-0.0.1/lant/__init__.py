from dataclasses import dataclass
from enum import Enum
from typing import Tuple
from pathlib import Path
from contextlib import contextmanager

import numpy as np
import cv2


def create_grid(dims: Tuple[int, int], init: str) -> np.ndarray:
    if init == "noise":
        rng = np.random.default_rng()
        grid = rng.integers(0, 2, size=dims, dtype="<?")
    else:
        grid = np.zeros(dims, dtype="<?")
        if init == "white":
            grid[...] = True
    return grid


def array_as_frame(array: np.ndarray, scale: int) -> np.ndarray:
    frame = array.astype("uint8") * 255
    return np.repeat(np.repeat(frame, scale, axis=0), scale, axis=1)


@contextmanager
def video_writer(path: Path, codec: str, rate: int, res: Tuple[int, int]):
    fourcc = cv2.VideoWriter_fourcc(*codec)
    video_file = cv2.VideoWriter(str(path), fourcc, rate, res, False)
    try:
        yield video_file
    finally:
        video_file.release()


class Direction(Enum):
    RIGHT = 0
    DOWN = 90
    LEFT = 180
    UP = 270


@dataclass
class Ant:
    __slots__ = "x", "y", "_angle"
    x: int
    y: int
    _angle: Direction

    def move(self, grid: np.ndarray) -> np.ndarray:
        cell = grid[self.y, self.x]
        grid[self.y, self.x] = ~cell
        # direction change
        if cell == True:
            self.angle = self.angle.value + 90
        else:
            self.angle = self.angle.value - 90
        # movement
        if self.angle == Direction.RIGHT:
            self.x += 1
        elif self.angle == Direction.DOWN:
            self.y += 1
        elif self.angle == Direction.LEFT:
            self.x -= 1
        elif self.angle == Direction.UP:
            self.y -= 1
        # release the updated grid
        return grid

    @property
    def angle(self) -> Direction:
        return self._angle

    @angle.setter
    def angle(self, val: int) -> None:
        self._angle = Direction(val % 360)

    def bounded(self, bounds: Tuple[int, int]) -> bool:
        by, bx = bounds
        return ((self.x >= 0) and (self.x < bx)
                and (self.y >= 0) and (self.y < by))
