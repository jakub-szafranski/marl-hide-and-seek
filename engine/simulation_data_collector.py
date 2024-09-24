from utils import calculate_episode_return, Logger

import json
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Board

log = Logger(__name__)

class SimulationVisualizer(ABC):
    @abstractmethod
    def collect_data(self, board: "Board") -> None:
        pass

    @abstractmethod
    def save_data(self, file_path: str) -> None:
        pass


class SimulationDataCollector(SimulationVisualizer):
    def __init__(self) -> None:
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

    def save_data(self, file_path: str) -> None:
        data = {
            "episode_lengths": self.episode_lengths,
            "hider_returns": self.hider_returns,
            "seeker_returns": self.seeker_returns,
        }

        log.info(f"Saving data to {file_path}.")
        with open(file_path, "w") as file:
            json.dump(data, file)
        log.info("Data saved successfully.")