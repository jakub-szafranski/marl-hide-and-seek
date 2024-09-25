from __future__ import annotations
from .learning_algorithm import LearningAlgorithm
from environment import Action

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import Trajectory


class QLearning(LearningAlgorithm):
    def __init__(
        self,
        learning_rate: float,
        discount_factor: float,
        default_q_value: float = 0.0,
        n_steps: int = 1,
    ) -> None:
        super().__init__(learning_rate, discount_factor, default_q_value)
        self.n_steps = n_steps

    def update(self, trajectory: Trajectory) -> None:
        number_of_transitions = len(trajectory)
        is_terminal = trajectory.transitions[-1].is_terminal

        # If the trajectory is not long enough, do not update the Q-values
        if (
            number_of_transitions < self.n_steps 
            and not is_terminal
            ):  
            return None
        
        n_step_trajectory = trajectory.get_sub_trajectory(self.n_steps)
        if is_terminal:
            for index, transition in enumerate(n_step_trajectory.transitions):
                self._update_q_values(n_step_trajectory[index:], is_terminal)
        else:
            self._update_q_values(n_step_trajectory, is_terminal)


    def _update_q_values(self, n_step_trajectory: Trajectory, is_terminal: bool) -> None:
        update_state = n_step_trajectory.transitions[0].state
        update_action = n_step_trajectory.transitions[0].action

        n_step_return = 0
        for i, transition in enumerate(n_step_trajectory.transitions):
            n_step_return += self.discount_factor ** i * transition.reward

        if not is_terminal:
            next_state = n_step_trajectory.transitions[-1].next_state
            max_q_value = max(
                self.q_values[next_state][action] for action in Action
            )
            n_step_return += self.discount_factor ** self.n_steps * max_q_value

        td_error = n_step_return - self.q_values[update_state][update_action]
        self.q_values[update_state][update_action] += self.learning_rate * td_error
