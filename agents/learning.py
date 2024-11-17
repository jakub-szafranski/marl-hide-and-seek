from __future__ import annotations
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import TYPE_CHECKING

from environment import Action

if TYPE_CHECKING:
    from agents import Trajectory


class LearningAlgorithm(ABC):
    def __init__(
        self,
        discount_factor: float,
        default_q_value: float,
    ) -> None:
        self.discount_factor = discount_factor
        self.q_values = defaultdict(lambda: defaultdict(lambda: default_q_value))

    @abstractmethod
    def update(self, trajectory: Trajectory) -> None:
        pass

    def load_prelearned_q_values(self, prelearned_q_values: dict) -> None:
        for state in prelearned_q_values:
            for action in prelearned_q_values[state]:
                self.q_values[state][action] = prelearned_q_values[state][action]


class MonteCarlo(LearningAlgorithm):
    def __init__(
        self,
        discount_factor: float,
        default_q_value: float = 0.0,
    ) -> None:
        super().__init__(discount_factor, default_q_value)
        self.visit_counts = defaultdict(lambda: defaultdict(int))

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
            self.visit_counts[state][action] += 1
            self.q_values[state][action] += (cumulative_reward - self.q_values[state][action]) / self.visit_counts[state][action]


class QLearning(LearningAlgorithm):
    def __init__(
        self,
        learning_rate: float = 0.05,
        discount_factor: float = 0.9,
        default_q_value: float = 0.0,
    ) -> None:
        super().__init__(discount_factor, default_q_value)
        self.learning_rate = learning_rate

    def update(self, trajectory: Trajectory) -> None:
        n_steps = 1
        number_of_transitions = len(trajectory)
        is_terminal = trajectory.transitions[-1].is_terminal

        # If the trajectory is not long enough, do not update the Q-values
        if (
            number_of_transitions < n_steps 
            and not is_terminal
            ):  
            return None
        
        n_step_trajectory = trajectory.get_sub_trajectory(n_steps)
        if is_terminal:
            for index, transition in enumerate(n_step_trajectory.transitions):
                self._update_q_values(n_step_trajectory[index:], is_terminal)
        else:
            self._update_q_values(n_step_trajectory, is_terminal)


    def _update_q_values(self, n_step_trajectory: Trajectory, is_terminal: bool) -> None:
        n_steps = 1
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
            n_step_return += self.discount_factor ** n_steps * max_q_value

        td_error = n_step_return - self.q_values[update_state][update_action]
        self.q_values[update_state][update_action] += self.learning_rate * td_error


class Sarsa(LearningAlgorithm):
    def __init__(
        self,
        learning_rate: float = 0.05,
        discount_factor: float = 0.9,
        default_q_value: float = 0.0,
    ) -> None:
        super().__init__(discount_factor, default_q_value)
        self.learning_rate = learning_rate

    def update(self, trajectory: Trajectory) -> None:
        n_steps = 1
        number_of_transitions = len(trajectory)
        is_terminal = trajectory.transitions[-1].is_terminal

        # If the trajectory is not long enough, do not update the Q-values
        if (
            number_of_transitions < n_steps + 1
            and not is_terminal
            ):  
            return None
        
        n_step_trajectory = trajectory.get_sub_trajectory(n_steps + 1)
        if is_terminal:
            for index, transition in enumerate(n_step_trajectory.transitions):
                self._update_q_values(n_step_trajectory[index:], is_terminal)
        else:
            self._update_q_values(n_step_trajectory, is_terminal)


    def _update_q_values(self, n_step_trajectory: Trajectory, is_terminal: bool) -> None:
        n_steps = 1
        update_state = n_step_trajectory.transitions[0].state
        update_action = n_step_trajectory.transitions[0].action

        if is_terminal:
            reward_trajectory = n_step_trajectory.transitions
        else:
            reward_trajectory = n_step_trajectory.transitions[:-1]

        n_step_return = 0
        for i, transition in enumerate(reward_trajectory):
            n_step_return += self.discount_factor ** i * transition.reward

        if not is_terminal:
            next_state = n_step_trajectory.transitions[-2].next_state
            next_action = n_step_trajectory.transitions[-1].action

            n_step_return += self.discount_factor ** n_steps * self.q_values[next_state][next_action]

        td_error = n_step_return - self.q_values[update_state][update_action]
        self.q_values[update_state][update_action] += self.learning_rate * td_error


class AlgorithmFactory:
    LEARNING_ALGORITHMS = {
        Sarsa.__name__: Sarsa,
        QLearning.__name__: QLearning,
        MonteCarlo.__name__: MonteCarlo
        }
    
    @staticmethod
    def get_algorithm(algorithm: str) -> LearningAlgorithm:
        if algorithm not in AlgorithmFactory.LEARNING_ALGORITHMS:
            raise ValueError(f"Algorithm {algorithm} not found")
        return AlgorithmFactory.LEARNING_ALGORITHMS[algorithm]
