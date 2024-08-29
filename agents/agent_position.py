from __future__ import annotations
from dataclasses import dataclass
import yaml
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Action

@dataclass
class AgentPosition:
    x: int
    y: int

    def __post_init__(self):
        with open('config.yml', 'r') as file:
            self.config = yaml.safe_load(file)

    def update(self, action: Action) -> None:
        if action == Action.UP:
            self.y = min(self.y + 1, self.config['grid_height'] - 1)
        elif action == Action.DOWN:
            self.y = max(self.y - 1, 0)
        elif action == Action.LEFT:
            self.x = max(self.x - 1, 0)
        elif action == Action.RIGHT:
            self.x = min(self.x + 1, self.config['grid_width'] - 1)