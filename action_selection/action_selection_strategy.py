from environment.action import Action
from environment.state import BaseState

from abc import ABC, abstractmethod


class ActionSelectionStrategy(ABC):
    @abstractmethod
    def select_action(self, state: BaseState, q_values) -> Action:
        pass
