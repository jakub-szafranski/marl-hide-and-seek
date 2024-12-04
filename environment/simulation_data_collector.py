from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Board
    from agents import Trajectory


class SimulationDataCollector:
    def __init__(self, data_file_path: str | None = None, q_values_file_path_hider: str = 'q_values_hider.json', q_values_file_path_seeker: str = 'q_values_seeker.json') -> None:
        self.data_file_path = data_file_path
        self.q_values_file_path_hider = q_values_file_path_hider
        self.q_values_file_path_seeker = q_values_file_path_seeker
        self.episode_lengths = []
        self.hider_returns = []
        self.seeker_returns = []
        self.hider_actions = []
        self.seeker_actions = []

    def collect_data(self, board: Board) -> None:
        hider_trajectory = board.hider.trajectory
        seeker_trajectory = board.seeker.trajectory

        if len(hider_trajectory) != len(seeker_trajectory):
            raise ValueError("Trajectories have different lengths.")


        self._collect_episode_length(hider_trajectory)
        self._collect_episode_returns(hider_trajectory, seeker_trajectory)
        self._collect_taken_actions(hider_trajectory, seeker_trajectory)
    
    def _collect_episode_length(self, hider_trajectory: Trajectory) -> None:
        self.episode_lengths.append(len(hider_trajectory) - 1)

    def _collect_episode_returns(self, hider_trajectory: Trajectory, seeker_trajectory: Trajectory) -> None:
        hider_return = self._calculate_episode_return(hider_trajectory)
        self.hider_returns.append(hider_return)

        seeker_return = self._calculate_episode_return(seeker_trajectory)
        self.seeker_returns.append(seeker_return)
    
    def _collect_taken_actions(self, hider_trajectory: Trajectory, seeker_trajectory: Trajectory) -> None:

        hider_actions = [transition.action.name for transition in hider_trajectory.transitions]
        seeker_actions = [transition.action.name for transition in seeker_trajectory.transitions]

        self.hider_actions.extend(hider_actions)
        self.seeker_actions.extend(seeker_actions)
    
    def _calculate_episode_return(self, trajectory: Trajectory) -> float:
        return sum(transition.reward for transition in trajectory.transitions)

    def _json_serializable_q_values(self, q_values: dict) -> dict:
        return {str(k): {action.value: v for action, v in actions.items()} for k, actions in q_values.items()}
    
    def save_data(self) -> None:
        data = {
            "episode_lengths": self.episode_lengths,
            "hider_returns": self.hider_returns,
            "seeker_returns": self.seeker_returns,
            "hider_actions": self.hider_actions,
            "seeker_actions": self.seeker_actions,
        }
        if self.data_file_path:
            print(f"Saving data to {self.data_file_path}.")
            with open(self.data_file_path, "w") as file:
                json.dump(data, file)
            print("Data saved successfully.")

    def save_q_values(self, board: Board) -> None:
        hider_q_values = board.hider.learning_algorithm.q_values
        hider_q_values = self._json_serializable_q_values(hider_q_values)

        seeker_q_values = board.seeker.learning_algorithm.q_values
        seeker_q_values = self._json_serializable_q_values(seeker_q_values)

        print(f"Saving Q-values to {self.q_values_file_path_hider}.")
        with open(self.q_values_file_path_hider, "w") as file:
            json.dump(hider_q_values, file)
        
        print(f"Saving Q-values to {self.q_values_file_path_seeker}.")
        with open(self.q_values_file_path_seeker, "w") as file:
            json.dump(seeker_q_values, file)