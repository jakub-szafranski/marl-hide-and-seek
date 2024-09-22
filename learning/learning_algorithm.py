from __future__ import annotations
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import Trajectory


class LearningAlgorithm(ABC):
    def __init__(
        self,
        learning_rate: float,
        discount_factor: float,
        default_q_value: float = 0.0,
    ) -> None:
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.q_values = defaultdict(lambda: defaultdict(lambda: default_q_value))

    @abstractmethod
    def update(self, trajectory: Trajectory) -> None:
        pass

