from __future__ import annotations
from abc import ABC, abstractmethod
from collections import defaultdict
import random
from typing import TYPE_CHECKING

from agents.action import Action
if TYPE_CHECKING:
    from environment import BaseState


class ActionSelectionStrategy(ABC):
    @abstractmethod
    def select_action(self, state: BaseState, q_values: defaultdict) -> Action:
        pass


class EpsilonGreedy(ActionSelectionStrategy):
    def __init__(self, epsilon: float) -> None:
        self.epsilon: float = epsilon

    def select_action(self, state: BaseState, q_values: defaultdict) -> Action:
        if random.random() < self.epsilon:
            return random.choice(list(Action))
        else:
            max_value = -float("inf")
            best_action = None
            for action in Action:
                if q_values[state][action] > max_value:
                    max_value = q_values[state][action]
                    best_action = action
            return best_action


class DecayEpsilonGreedy(ActionSelectionStrategy):
    def __init__(
            self, 
            epsilon: float, 
            min_epsilon: float, 
            decay_steps: int
            ) -> None:
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.decay_steps = decay_steps
        self.step = 0

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
        
        # Linear decrease epsilon
        if self.step < self.decay_steps:
            self.epsilon -= (self.epsilon - self.min_epsilon) / (self.decay_steps - self.step)
            self.step += 1
        
        return action
    

class ActionSelectionFactory:
    ACTION_SELECTION_STRATEGIES = {
        EpsilonGreedy.__name__: EpsilonGreedy,
        DecayEpsilonGreedy.__name__: DecayEpsilonGreedy,
    }

    @staticmethod
    def get_strategy(action_selection: str):
        if action_selection not in ActionSelectionFactory.ACTION_SELECTION_STRATEGIES:
            raise ValueError(f"Action selection {action_selection} not found")
        return ActionSelectionFactory.ACTION_SELECTION_STRATEGIES[action_selection]