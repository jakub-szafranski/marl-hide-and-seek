from __future__ import annotations
import yaml
import numpy as np
import random
from enum import Enum
from typing import TYPE_CHECKING

from src.agents import AgentPosition

if TYPE_CHECKING:
    from src.agents import Agent, AgentRole
    from src.agents.action import Action


class GridCell(Enum):
    EMPTY = 0
    HIDER = 1
    SEEKER = 2
    WALL = 3
    SEEKER_VISION = 4
    HIDER_FOUND = 5


class BoardBuilder:
    @staticmethod
    def build_grid(hider: Agent, seeker: Agent, config: dict, initialize_coordinates: bool = True) -> np.ndarray:
        if initialize_coordinates:
            BoardBuilder._initialize_agents_positions(hider=hider, seeker=seeker, config=config)

        grid = np.zeros((config["grid_height"], config["grid_width"]))
        wall_positions = config["walls"]

        if hider.position and seeker.position:
            detection_distance = config["detection_distance"]
            BoardBuilder._draw_seeker_vision(grid, seeker, detection_distance, wall_positions)

            grid[seeker.position.x, seeker.position.y] = GridCell.SEEKER.value
            if grid[hider.position.x, hider.position.y] == GridCell.SEEKER_VISION.value:
                grid[hider.position.x, hider.position.y] = GridCell.HIDER_FOUND.value
            else:
                grid[hider.position.x, hider.position.y] = GridCell.HIDER.value

        for wall_position in wall_positions:
            x, y = wall_position
            grid[x, y] = GridCell.WALL.value

        return grid

    @staticmethod
    def _initialize_agents_positions(hider: Agent, seeker: Agent, config: dict) -> None:
        hider_position, seeker_position = BoardBuilder._generate_start_coordinates(config)
        hider.position = hider_position
        seeker.position = seeker_position

    @staticmethod
    def _draw_seeker_vision(grid: np.ndarray, seeker: Agent, seeker_vision: int, wall_positions) -> np.ndarray:
        seeker_position = seeker.position
        for i in range(-seeker_vision, seeker_vision + 1):
            for j in range(-seeker_vision, seeker_vision + 1):
                if (
                    0 <= seeker_position.x + i < grid.shape[0]
                    and 0 <= seeker_position.y + j < grid.shape[1]
                    and not BoardBuilder._is_line_blocked(
                        (seeker_position.x, seeker_position.y),
                        (seeker_position.x + i, seeker_position.y + j),
                        wall_positions,
                    )
                ):
                    grid[seeker_position.x + i, seeker_position.y + j] = GridCell.SEEKER_VISION.value

    @staticmethod
    def _is_line_blocked(start, end, wall_positions):
        x0, y0 = start
        x1, y1 = end
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            if [x0, y0] in wall_positions:
                return True
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return False

    def _generate_start_coordinates(config) -> tuple[AgentPosition, AgentPosition]:
        grid_height = config["grid_height"]
        grid_width = config["grid_width"]
        detection_distance = config["detection_distance"]
        wall_positions = config["walls"]

        while True:
            hider_x = random.randint(0, grid_width - 1)
            hider_y = random.randint(0, grid_height - 1)

            seeker_x = random.randint(0, grid_width - 1)
            seeker_y = random.randint(0, grid_height - 1)

            if (
                [hider_x, hider_y] not in wall_positions
                and [seeker_x, seeker_y] not in wall_positions
                and abs(hider_x - seeker_x) > detection_distance + 1
                and abs(hider_y - seeker_y) > detection_distance + 1
            ):
                return AgentPosition(hider_x, hider_y), AgentPosition(seeker_x, seeker_y)


class Board:
    def __init__(self, hider: Agent, seeker: Agent) -> None:
        with open("config.yml", "r") as file:
            self.config = yaml.safe_load(file)

        self.hider = hider
        self.seeker = seeker

        self.grid = BoardBuilder.build_grid(
            hider=self.hider,
            seeker=self.seeker,
            config=self.config,
            initialize_coordinates=True,
        )

    def get_agent_state(self, agent: Agent) -> tuple:
        return agent.state_processor.get_state(self)

    def get_agent_action(self, agent: Agent, state: tuple) -> Action:
        return agent.select_action(state)

    def get_agent_reward(self, agent: Agent) -> float:
        return agent.reward_strategy.get_reward()

    def is_terminal(self) -> tuple[bool, AgentRole | None]:
        is_seeker_terminal, winner = self.seeker.state_processor.is_terminal(self)
        is_hider_terminal, winner = self.hider.state_processor.is_terminal(self)
        return is_seeker_terminal or is_hider_terminal, winner

    def add_agent_transition(
        self, agent: Agent, state: tuple, action: Action, reward: float, new_state: tuple, is_terminal: bool
    ) -> None:
        agent.trajectory.add_transition(state, action, reward, new_state, is_terminal)

    def update_grid(self, initialize_coordinates: bool = False) -> None:
        self.grid = BoardBuilder.build_grid(
            hider=self.hider,
            seeker=self.seeker,
            config=self.config,
            initialize_coordinates=initialize_coordinates,
        )

    def update_agents(self) -> None:
        self.hider.update()
        self.seeker.update()

    def reset(self) -> None:
        self.hider.reset()
        self.seeker.reset()
        self.update_grid(initialize_coordinates=True)
