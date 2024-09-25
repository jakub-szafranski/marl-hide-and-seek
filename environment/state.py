from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Board, BaseTerminalState


class BaseState(ABC):
    def __init__(self, terminal_state: BaseTerminalState) -> None:
        self._terminal_state = terminal_state

    @abstractmethod
    def get_state(self, board: Board) -> tuple:
        pass

    def is_terminal(self, board: Board) -> bool:
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
        )
    

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
