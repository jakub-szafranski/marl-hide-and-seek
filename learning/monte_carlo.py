from __future__ import annotations
from .learning_algorithm import LearningAlgorithm

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import Trajectory


class MonteCarlo(LearningAlgorithm):
    def __init__(
        self,
        learning_rate: float,
        discount_factor: float,
        default_q_value: float = 0.0,
    ) -> None:
        super().__init__(learning_rate, discount_factor, default_q_value)

    def update(self, trajectory: Trajectory) -> None:
        # Update only if the trajectory is complete
        if not trajectory.transitions[-1].is_terminal:
            return None
        
        cumulative_reward = 0 
        for transition in reversed(trajectory.transitions):
            state = transition.state
            action = transition.action
            reward = transition.reward

            cumulative_reward = reward + self.discount_factor * cumulative_reward  
            self.q_values[state][action] += self.learning_rate * (cumulative_reward - self.q_values[state][action])