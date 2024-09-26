from __future__ import annotations
from utils import calculate_episode_return, Logger, json_serializable_q_values

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Board

log = Logger(__name__)


class SimulationDataCollector:
    def __init__(self, data_file_path: str = 'simulation_data.json', q_values_file_path: str = 'q_values.json') -> None:
        self.data_file_path = data_file_path
        self.q_values_file_path = q_values_file_path
        self.episode_lengths = []
        self.hider_returns = []
        self.seeker_returns = []


    def collect_data(self, board: Board) -> None:
        hider_trajectory = board.hider.trajectory
        seeker_trajectory = board.seeker.trajectory

        if len(hider_trajectory) != len(seeker_trajectory):
            raise ValueError("Trajectories have different lengths.")

        self.episode_lengths.append(len(hider_trajectory))

        hider_return = calculate_episode_return(hider_trajectory)
        self.hider_returns.append(hider_return)

        seeker_return = calculate_episode_return(seeker_trajectory)
        self.seeker_returns.append(seeker_return)

    def save_data(self) -> None:
        data = {
            "episode_lengths": self.episode_lengths,
            "hider_returns": self.hider_returns,
            "seeker_returns": self.seeker_returns,
        }

        log.info(f"Saving data to {self.data_file_path}.")
        with open(self.data_file_path, "w") as file:
            json.dump(data, file)
        log.info("Data saved successfully.")

    def save_q_values(self, board: Board) -> None:
        hider_q_values = board.hider.learning_algorithm.q_values
        hider_q_values = json_serializable_q_values(hider_q_values)

        seeker_q_values = board.seeker.learning_algorithm.q_values
        seeker_q_values = json_serializable_q_values(seeker_q_values)

        data = {
            "hider_q_values": hider_q_values,
            "seeker_q_values": seeker_q_values,
        }

        log.info(f"Saving Q-values to {self.q_values_file_path}.")
        with open(self.q_values_file_path, "w") as file:
            json.dump(data, file)
        log.info("Q-values saved successfully.")