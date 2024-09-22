from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import yaml

if TYPE_CHECKING:
    from environment import Board


class BaseTerminalState(ABC):
    @abstractmethod
    def is_terminal(self, board: Board) -> bool:
        pass


class DetectionTerminalState(BaseTerminalState):
    def __init__(self) -> None:
        with open("config.yml", "r") as file:
            self.config = yaml.safe_load(file)
        self.detection_distance = self.config["detection_distance"]

    def is_terminal(self, board: Board) -> bool:
        hider_position = board.hider.position
        seeker_position = board.seeker.position
        if (
            abs(hider_position.x - seeker_position.x) <= self.detection_distance 
            and abs(hider_position.y - seeker_position.y) <= self.detection_distance
            ):
            return True
        return False
    

class TerminalStateFactory:
    TERMINAL_STATES = {DetectionTerminalState.__name__: DetectionTerminalState}
    
    @staticmethod
    def get_terminal_state(terminal_state: str) -> BaseTerminalState:
        if terminal_state not in TerminalStateFactory.TERMINAL_STATES:
            raise ValueError(f"Terminal state {terminal_state} not found")
        return TerminalStateFactory.TERMINAL_STATES[terminal_state]()