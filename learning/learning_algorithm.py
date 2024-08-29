from __future__ import annotations
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import Trajectory
    from environment import Action, BaseState


class LearningAlgorithm(ABC):
    def __init__(
        self,
        learning_rate: float,
        discount_factor: float,
    ) -> None:
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_values = defaultdict(float)

    @abstractmethod
    def update(self, trajectory: Trajectory) -> None:
        pass

    @abstractmethod
    def get_value(self, state: BaseState, action: Action) -> float:
        return self.q_values[(state, action)]
        # should it be a method that returns all q_values for a given state?
        # should it be a method that returns the best action for a given state?

