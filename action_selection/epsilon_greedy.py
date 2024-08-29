from __future__ import annotations
from typing import TYPE_CHECKING
from action_selection.action_selection_strategy import ActionSelectionStrategy

if TYPE_CHECKING:
    from environment.state import BaseState, Action

class EpsilonGreedy(ActionSelectionStrategy):
    def __init__(self, epsilon: float) -> None:
        self.epsilon: float = epsilon

    def select_action(self, state: BaseState, q_values) -> Action:
        pass