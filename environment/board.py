from __future__ import annotations
import yaml
from enum import Enum
import numpy as np
from typing import TYPE_CHECKING

from utils import generate_start_coordinates

if TYPE_CHECKING:
    from agents import Agent
    from environment import Action


class GridCell(Enum):
    EMPTY = 0
    HIDER = 1
    SEEKER = 2
    WALL = 3


class BoardBuilder:
    @staticmethod
    def build_grid(hider: Agent, seeker: Agent, config: dict, initialize_coordinates: bool = True) -> np.ndarray:
        if initialize_coordinates:
            BoardBuilder._initialize_agents_positions(hider=hider, seeker=seeker)
        
        grid = np.zeros((config["grid_height"], config["grid_width"]))
        for wall_position in config["walls"]:
            x, y = wall_position
            grid[x, y] = GridCell.WALL.value

        if hider.position and seeker.position:
            grid[hider.position.x, hider.position.y] = GridCell.HIDER.value
            grid[seeker.position.x, seeker.position.y] = GridCell.SEEKER.value

        return grid

    @staticmethod
    def _initialize_agents_positions(hider: Agent, seeker: Agent) -> None:
        hider_position, seeker_position = generate_start_coordinates()
        hider.position = hider_position
        seeker.position = seeker_position


class Board:
    def __init__(self, hider: Agent, seeker: Agent,) -> None:
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
    
    def get_agent_reward(self, agent: Agent, state: tuple, action: Action, new_state: tuple) -> float:
        return agent.reward_strategy.get_reward(state, action, new_state)
    
    def is_terminal(self) -> bool:
        return self.seeker.state_processor.is_terminal(self) or self.hider.state_processor.is_terminal(self)
    
    def add_agent_transition(self, agent: Agent, state: tuple, action: Action, reward: float, new_state: tuple, is_terminal: bool) -> None:
        agent.trajectory.add_transition(state, action, reward, new_state, is_terminal)

    def _update_grid(self, initialize_coordinates: bool = False) -> None:
        self.grid = BoardBuilder.build_grid(
            hider=self.hider,
            seeker=self.seeker,
            config=self.config,
            initialize_coordinates=initialize_coordinates,
            )
        
    def update(self) -> None:
        self.hider.update()
        self.seeker.update()
        self._update_grid()

    def reset(self) -> None:
        self.hider.reset()
        self.seeker.reset()
        self._update_grid(initialize_coordinates=True)      



