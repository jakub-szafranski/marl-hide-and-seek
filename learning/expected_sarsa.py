from __future__ import annotations
from .learning_algorithm import LearningAlgorithm

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import Trajectory


class ExpectedSarsa(LearningAlgorithm):
    def __init__(
        self,
        learning_rate: float,
        discount_factor: float,
        default_q_value: float = 0.0,
    ) -> None:
        super().__init__(learning_rate, discount_factor, default_q_value)

    def update(self, trajectory: Trajectory) -> None:
        raise NotImplementedError
