from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Board


class BaseTerminalState(ABC):
    @abstractmethod
    def is_terminal(self, board: Board) -> bool:
        pass


class TerminalState(BaseTerminalState):
    def is_terminal(self, board: Board) -> bool:
        return board.hider.position == board.seeker.position
    

class TerminalStateFactory:
    TERMINAL_STATES = {TerminalState.__name__: TerminalState}
    
    @staticmethod
    def get_terminal_state(terminal_state: str) -> BaseTerminalState:
        return TerminalStateFactory.TERMINAL_STATES[terminal_state]()