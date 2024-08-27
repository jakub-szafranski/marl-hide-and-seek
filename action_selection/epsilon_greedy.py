from .action_selection_strategy import SelectionAlgorithm
from environment.state import BaseState

from environment.action import Action


class EpsilonGreedy(SelectionAlgorithm):
    def __init__(self, epsilon: float) -> None:
        self.epsilon: float = epsilon

    def select_action(self, state: BaseState, q_values) -> Action:
        pass