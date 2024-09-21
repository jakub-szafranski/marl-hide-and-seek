from __future__ import annotations
import random
from typing import TYPE_CHECKING
from collections import defaultdict

from environment import Action
from .action_selection_strategy import ActionSelectionStrategy

if TYPE_CHECKING:
    from environment.state import BaseState


class DecayEpsilonGreedy(ActionSelectionStrategy):
    def __init__(
            self, 
            initial_epsilon: float, 
            decay_rate: float, 
            min_epsilon: float = 0,
            ) -> None:
        self.epsilon = initial_epsilon
        self.decay_rate = decay_rate
        self.min_epsilon = min_epsilon

    def select_action(self, state: BaseState, q_values: defaultdict) -> Action:
        if random.random() < self.epsilon:
            action = random.choice(list(Action))
        else:
            max_value = -float("inf")
            best_action = None
            for action in Action:
                if q_values[state][action] > max_value:
                    max_value = q_values[state][action]
                    best_action = action
            action = best_action
        
        # Decay epsilon
        self.epsilon = max(self.min_epsilon, self.epsilon * self.decay_rate)
        
        return action