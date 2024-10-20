from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from environment import Action

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


class CompleteKnowledgeState(BaseState):
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
    

class PartialKnowledgeHider(BaseState):
    def __init__(self, terminal_state: BaseTerminalState) -> None:
        super().__init__(terminal_state)
    
    def get_state(self, board: Board) -> tuple:
        hider = board.hider
        hider_x = hider.position.x
        hider_y = hider.position.y
        transition_number = len(hider.trajectory)

        seeker = board.seeker
        seeker_x = seeker.position.x
        seeker_y = seeker.position.y
        is_above = 1 if seeker_y < hider_y else 0
        is_below = 1 if seeker_y > hider_y else 0
        is_right = 1 if seeker_x > hider_x else 0
        is_left = 1 if seeker_x < hider_x else 0
        return (is_above, is_below, is_right, is_left, transition_number, hider_x, hider_y)


class PartialKnowledgeSeeker(BaseState):
    def __init__(self, terminal_state: BaseTerminalState) -> None:
        super().__init__(terminal_state)

    def get_state(self, board: Board) -> tuple:
        seeker = board.seeker
        seeker_x = seeker.position.x
        seeker_y = seeker.position.y
        transition_number = len(seeker.trajectory)

        hider = board.hider
        hider_x = hider.position.x
        hider_y = hider.position.y
        is_above = 1 if seeker_y < hider_y else 0
        is_below = 1 if seeker_y > hider_y else 0
        is_right = 1 if seeker_x > hider_x else 0
        is_left = 1 if seeker_x < hider_x else 0
        return (is_above, is_below, is_right, is_left, transition_number, seeker_x, seeker_y)
    

class DistanceStateSeeker(BaseState):
    def __init__(self, terminal_state: BaseTerminalState) -> None:
        super().__init__(terminal_state)
    
    def get_state(self, board: Board) -> tuple:
        seeker_position = board.seeker.position
        hider_position = board.hider.position
        transition_number = len(board.seeker.directory)
        x_distance = seeker_position.x - hider_position.x
        y_distance = seeker_position.y - hider_position.y
        return (x_distance, y_distance, transition_number, seeker_position.x, seeker_position.y)
    

class DistanceStateSeeker(BaseState):
    def __init__(self, terminal_state: BaseTerminalState) -> None:
        super().__init__(terminal_state)
    
    def get_state(self, board: Board) -> tuple:
        seeker_position = board.seeker.position
        hider_position = board.hider.position
        transition_number = len(board.seeker.directory)
        x_distance = seeker_position.x - hider_position.x
        y_distance = seeker_position.y - hider_position.y
        return (x_distance, y_distance, transition_number, hider_position.x, hider_position.y)
    

class HearingStateHider(BaseState):
    def __init__(self, terminal_state: BaseTerminalState) -> None:
        super().__init__(terminal_state)
    
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
    def __init__(self, terminal_state: BaseTerminalState) -> None:
        super().__init__(terminal_state)

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
        PartialKnowledgeSeeker.__name__: PartialKnowledgeSeeker,
        HearingStateSeeker.__name__: HearingStateSeeker,
        }
    HIDER_STATES = {
        CompleteKnowledgeState.__name__: CompleteKnowledgeState,
        PartialKnowledgeHider.__name__: PartialKnowledgeHider,
        HearingStateHider.__name__: HearingStateHider,
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
