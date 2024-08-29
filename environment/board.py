from __future__ import annotations
import yaml
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import Agent, AgentPosition
    from utils import generate_start_coordinates


class Board:
    def __init__(self, hider: Agent, seeker: Agent) -> None:
        with open("config.yml", "r") as file:
            self.config = yaml.safe_load(file)

        self.hider = hider
        self.seeker = seeker

        self.grid = self._build_grid()

    def _build_grid(self):
        pass

    def update_grid(self) -> None:
        self.grid = self._build_grid()

    def display(self):
        pass
