from __future__ import annotations
from abc import ABC, abstractmethod
import yaml
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Board, BaseTerminalState
    from agents import AgentRole


class BaseState(ABC):
    def __init__(self, terminal_state: BaseTerminalState) -> None:
        self._terminal_state = terminal_state

    @abstractmethod
    def get_state(self, board: Board) -> tuple:
        pass

    def is_terminal(self, board: Board) -> tuple[bool, AgentRole | None]:
        return self._terminal_state.is_terminal(board)


class CoordinateState(BaseState):
    def __init__(self, terminal_state: BaseTerminalState) -> None:
        super().__init__(terminal_state)

    def get_state(self, board: Board) -> tuple:
        return (
            board.hider.position.x, 
            board.hider.position.y, 
            board.seeker.position.x, 
            board.seeker.position.y,
            len(board.seeker.trajectory)
        )
    

class SeekerVisionState(BaseState):
    def __init__(self, terminal_state: BaseTerminalState, seeker_view_distance: int = 2) -> None:
        super().__init__(terminal_state)
        self.seeker_view_distance = seeker_view_distance

    def get_state(self, board: Board) -> tuple:
        seeker = board.seeker

        grid = board.grid
        seeker_x = seeker.position.x
        seeker_y = seeker.position.y

        seeker_upper_bound = min(seeker_y + self.seeker_view_distance, grid.shape[0])
        seeker_lower_bound = max(seeker_y - self.seeker_view_distance, 0)
        seeker_left_bound = max(seeker_x - self.seeker_view_distance, 0)
        seeker_right_bound = min(seeker_x + self.seeker_view_distance, grid.shape[1])

        seeker_view = grid[seeker_lower_bound:seeker_upper_bound + 1, seeker_left_bound:seeker_right_bound + 1]
        seeker_view = seeker_view.flatten()
        seeker_view = seeker_view.tolist()
        seeker_view.append(len(seeker.trajectory))
        return tuple(seeker_view)

    

class StateFactory():
    SEEKER_STATES = {CoordinateState.__name__: CoordinateState,}
    HIDER_STATES = {CoordinateState.__name__: CoordinateState,}

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
