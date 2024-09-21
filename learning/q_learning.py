from .learning_algorithm import LearningAlgorithm

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import Trajectory
    from environment import Action, BaseState


class QLearning(LearningAlgorithm):
    def __init__(
        self,
        learning_rate: float,
        discount_factor: float,
        n_steps: int,
    ) -> None:
        super().__init__(learning_rate, discount_factor)
        self.n_steps = n_steps

    def update(self, trajectory: Trajectory) -> None:
        number_of_transitions = len(trajectory)

        # If the trajectory is not long enough, do not update the Q-values
        if number_of_transitions < self.n_steps:  
            return None
        
        n_step_trajectory = trajectory.get_sub_trajectory(self.n_steps)
        
        update_state = n_step_trajectory.transitions[0].state
        update_action = n_step_trajectory.transitions[0].action

        n_step_return = 0
        for i in range(self.n_steps):
            if len(n_step_trajectory) < i:
                break
            n_step_return += self.discount_factor ** i * n_step_trajectory.transitions[i].reward

        if not n_step_trajectory.transitions[-1].is_terminal:
            next_state = n_step_trajectory.transitions[-1].next_state
            max_q_value = max(
                self.q_values[next_state][action] for action in Action
            )
            n_step_return += self.discount_factor ** self.n_steps * max_q_value

        td_error = n_step_return - self.q_values[update_state][update_action]
        self.q_values[update_state][update_action] += self.learning_rate * td_error
