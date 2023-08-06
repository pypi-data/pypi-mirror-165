#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from typing import Tuple

import click
import numpy as np

from . import Ant, Direction, video_writer, array_as_frame, create_grid


@click.command()
@click.argument("max-steps", type=click.IntRange(1, None))
@click.argument("output", type=click.Path(readable=False, writable=True,
                                          path_type=Path))
@click.option("--init", default="white", show_default=True,
              type=click.Choice(["black", "white", "noise"],
                                case_sensitive=False))
@click.option("--grid-size", nargs=2, default=(250, 250),
              type=click.IntRange(10, None, clamp=True), show_default=True)
@click.option("--scale", type=click.IntRange(None, 10), show_default=True,
              default=4, help="Factor by which to rescale the grid for video.")
@click.option("--rate", type=click.INT, default=300, show_default=True)
def main(max_steps: int, output: Path, init: str,
         grid_size: Tuple[int, int], scale: int, rate: int) -> None:
    if output.exists() and not click.confirm(f"{output} exists! Overwrite?"):
        raise click.Abort()
    bound_y, bound_x = grid_size
    res = tuple((x * scale for x in grid_size))
    grid = create_grid(grid_size, init)
    ant = Ant(bound_x // 2, bound_y // 2, Direction.RIGHT)
    with video_writer(output, "mp4v", rate, res) as video_file:
        for _ in range(max_steps):
            if not ant.bounded(grid_size):
                break
            grid = ant.move(grid)
            video_file.write(array_as_frame(grid, scale))


if __name__ == "__main__":
    sys.exit(main())
