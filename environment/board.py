from agents.agent import Agent
from agents.agent_position import AgentPosition

import yaml


class Board:
    def __init__(self, hider, seeker) -> None:
        with open('config.yml', 'r') as file:
            self.config = yaml.safe_load(file)

        self.hider = hider
        self.seeker = seeker

        self.grid = self._build_grid()
        
    def _build_grid(self):
        pass

    def _get_agent_position(self, agent: Agent) -> AgentPosition:
        return agent.agent_position

    def update_grid(self) -> None:
        self.grid = self._build_grid()

    def display(self):
        pass






    