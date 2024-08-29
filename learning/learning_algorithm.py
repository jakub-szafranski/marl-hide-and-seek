from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import Trajectory


class LearningAlgorithm(ABC):
    def __init__(
        self,
        learning_rate: float,
        discount_factor: float,
        epsilon: float,
    ) -> None:
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

    @abstractmethod
    def update(self, trajectory: Trajectory) -> None:
        pass

    @abstractmethod
    def get_value(self, state) -> float:
        pass
