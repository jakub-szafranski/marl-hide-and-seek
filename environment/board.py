from __future__ import annotations
import yaml
from enum import Enum
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import Agent
    from utils import generate_start_coordinates


class GridCell(Enum):
    EMPTY = 0
    HIDER = 1
    SEEKER = 2
    WALL = 3


class Board:
    def __init__(self, hider: Agent, seeker: Agent) -> None:
        with open("config.yml", "r") as file:
            self.config = yaml.safe_load(file)

        self.hider = hider
        self.seeker = seeker

        self.grid = self.build_grid()

    def build_grid(self, initialize_coordinates: bool = True) -> np.ndarray:
        if initialize_coordinates:
            self._initialize_agents_positions()
        
        grid = np.zeros((self.config["grid_height"], self.config["grid_width"]))
        for wall_position in self.config["walls"]:
            x, y = wall_position
            grid[x, y] = GridCell.WALL.value

        if self.hider.position and self.seeker.position:
            grid[self.hider.position.x, self.hider.position.y] = GridCell.HIDER.value
            grid[self.seeker.position.x, self.seeker.position.y] = GridCell.SEEKER.value

        return grid

    def update_grid(self) -> None:
        self.grid = self._build_grid(initialize_coordinates=False)

    def _initialize_agents_positions(self) -> None:
        hider_position, seeker_position = generate_start_coordinates()
        self.hider.position = hider_position
        self.seeker.position = seeker_position

    def reset(self) -> None:
        self.hider.reset()
        self.seeker.reset()
        self.update_grid()        



