from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import yaml

from utils import Logger
from agents import AgentRole

if TYPE_CHECKING:
    from environment import Board

log = Logger(__name__)

class BaseTerminalState(ABC):
    @abstractmethod
    def is_terminal(self, board: Board) -> tuple[bool, AgentRole | None]:
        pass


class DetectionTerminalState(BaseTerminalState):
    def __init__(self) -> None:
        with open("config.yml", "r") as file:
            self.config = yaml.safe_load(file)
        self.detection_distance = self.config["detection_distance"]
        self.max_steps = self.config["max_steps"]
        self.walls = self.config["walls"]

    def is_terminal(self, board: Board) -> tuple[bool, AgentRole | None]:
        hider_position = board.hider.position
        seeker_position = board.seeker.position
        winner = None

        if (
            abs(hider_position.x - seeker_position.x) <= self.detection_distance 
            and abs(hider_position.y - seeker_position.y) <= self.detection_distance
            ):
            winner = AgentRole.SEEKER
            return True, winner
        
        current_step_number = len(board.seeker.trajectory)
        if current_step_number >= self.max_steps:
            winner = AgentRole.HIDER
            return True, winner
        return False, winner
    

class TerminalStateFactory:
    TERMINAL_STATES = {DetectionTerminalState.__name__: DetectionTerminalState}
    
    @staticmethod
    def get_terminal_state(terminal_state: str) -> BaseTerminalState:
        if terminal_state not in TerminalStateFactory.TERMINAL_STATES:
            raise ValueError(f"Terminal state {terminal_state} not found")
        return TerminalStateFactory.TERMINAL_STATES[terminal_state]