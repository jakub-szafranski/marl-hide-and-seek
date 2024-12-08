from __future__ import annotations
from abc import ABC, abstractmethod
import yaml
from typing import TYPE_CHECKING

from agents.action import Action 
from agents import AgentRole

if TYPE_CHECKING:
    from environment import Board


class TerminalState:
    def __init__(self) -> None:
        with open("config.yml", "r") as file:
            self.config = yaml.safe_load(file)
        self.detection_distance = self.config["detection_distance"]
        self.max_steps = self.config["max_steps"]
        self.walls = self.config["walls"]

    def is_terminal(self, board: Board) -> tuple[bool, AgentRole | None]:
        hider_position = board.hider.position
        is_found = board.grid[hider_position.x, hider_position.y] == 5
        winner = None

        if is_found:
            winner = AgentRole.SEEKER
            return True, winner
        
        current_step_number = len(board.seeker.trajectory)
        if current_step_number >= self.max_steps:
            winner = AgentRole.HIDER
            return True, winner
        return False, winner


class BaseState(ABC):
    def __init__(self) -> None:
        self._terminal_state = TerminalState()

    @abstractmethod
    def get_state(self, board: Board) -> tuple:
        pass

    def is_terminal(self, board: Board) -> tuple[bool, AgentRole | None]:
        return self._terminal_state.is_terminal(board)


class CompleteKnowledgeState(BaseState):
    def __init__(self) -> None:
        super().__init__()

    def get_state(self, board: Board) -> tuple:
        return (
            board.hider.position.x, 
            board.hider.position.y, 
            board.seeker.position.x, 
            board.seeker.position.y,
            len(board.seeker.trajectory)
        )
    

class DistanceStateSeeker(BaseState):
    def __init__(self) -> None:
        super().__init__()
    
    def get_state(self, board: Board) -> tuple:
        seeker_position = board.seeker.position
        hider_position = board.hider.position
        transition_number = len(board.seeker.trajectory)
        x_distance = seeker_position.x - hider_position.x
        y_distance = seeker_position.y - hider_position.y
        return (x_distance, y_distance, transition_number, seeker_position.x, seeker_position.y)
    

class DistanceStateHider(BaseState):
    def __init__(self) -> None:
        super().__init__()
    
    def get_state(self, board: Board) -> tuple:
        seeker_position = board.seeker.position
        hider_position = board.hider.position
        transition_number = len(board.seeker.trajectory)
        x_distance = seeker_position.x - hider_position.x
        y_distance = seeker_position.y - hider_position.y
        return (x_distance, y_distance, transition_number, hider_position.x, hider_position.y)
    

class HearingStateHider(BaseState):
    def __init__(self) -> None:
        super().__init__()
    
    def get_state(self, board: Board) -> tuple:
        hider = board.hider
        hider_x = hider.position.x
        hider_y = hider.position.y
        transition_number = len(hider.trajectory)

        seeker = board.seeker
        seeker_x = seeker.position.x
        seeker_y = seeker.position.y
        if (
            seeker.trajectory.transitions and 
            seeker.trajectory.transitions[-1].action == Action.STAY
            ):
            is_above, is_below, is_right, is_left = -1, -1, -1, -1
        else:
            is_above = 1 if seeker_y > hider_y else 0
            is_below = 1 if seeker_y < hider_y else 0
            is_right = 1 if seeker_x > hider_x else 0
            is_left = 1 if seeker_x < hider_x else 0
        return (is_above, is_below, is_right, is_left, transition_number, hider_x, hider_y)


class HearingStateSeeker(BaseState):
    def __init__(self) -> None:
        super().__init__()

    def get_state(self, board: Board) -> tuple:
        seeker = board.seeker
        seeker_x = seeker.position.x
        seeker_y = seeker.position.y
        transition_number = len(seeker.trajectory)

        hider = board.hider
        hider_x = hider.position.x
        hider_y = hider.position.y
        if (
            hider.trajectory.transitions and 
            hider.trajectory.transitions[-1].action == Action.STAY
            ):
            is_above, is_below, is_right, is_left = -1, -1, -1, -1
        else:
            is_above = 1 if seeker_y < hider_y else 0
            is_below = 1 if seeker_y > hider_y else 0
            is_right = 1 if seeker_x < hider_x else 0
            is_left = 1 if seeker_x > hider_x else 0
        return (is_above, is_below, is_right, is_left, transition_number, seeker_x, seeker_y)
    

class StateFactory():
    SEEKER_STATES = {
        CompleteKnowledgeState.__name__: CompleteKnowledgeState,
        HearingStateSeeker.__name__: HearingStateSeeker,
        DistanceStateSeeker.__name__: DistanceStateSeeker,
        }
    HIDER_STATES = {
        CompleteKnowledgeState.__name__: CompleteKnowledgeState,
        HearingStateHider.__name__: HearingStateHider,
        DistanceStateHider.__name__: DistanceStateHider,
        }

    @staticmethod
    def get_seeker_state(state_name: str) -> BaseState:
        if state_name not in StateFactory.SEEKER_STATES:
            raise ValueError(f"State {state_name} not found")
        return StateFactory.SEEKER_STATES[state_name]
    
    @staticmethod
    def get_hider_state(state_name: str) -> BaseState:
        if state_name not in StateFactory.HIDER_STATES:
            raise ValueError(f"State {state_name} not found")
        return StateFactory.HIDER_STATES[state_name]
