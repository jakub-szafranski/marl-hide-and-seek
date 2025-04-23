from __future__ import annotations
from .simulation_visualizer import SimulationVisualizer
from .simulation_data_collector import SimulationDataCollector
from src.utils.logger import get_logger

import yaml
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .board import Board


class Simulation:
    def __init__(
        self,
        board: Board,
        simulation_visualizer: SimulationVisualizer = None,
        simulation_data_collector: SimulationDataCollector = None,
    ) -> None:
        self.board = board
        self.simulation_visualizer = simulation_visualizer
        self.simulation_data_collector = simulation_data_collector
        self.log = get_logger("Simulation")

        with open("config.yml", "r") as file:
            self.config = yaml.safe_load(file)

    def run(self) -> None:
        total_episodes = self.config["total_episodes"]
        self.log.info(f"Running simulation for {total_episodes} episodes.")
        for episode in range(total_episodes):
            print(f"Running episode {episode}.", end="\r")
            self._run_episode()
            self._reset()

        if self.simulation_data_collector:
            self.simulation_data_collector.save_q_values(self.board)
            self.simulation_data_collector.save_data()

    def _run_episode(self) -> None:
        """Run a single episode of the simulation."""
        episode_finished = False
        while not episode_finished:
            episode_finished = self._run_step()

        if self.simulation_data_collector:
            self.simulation_data_collector.collect_data(self.board)

    def _run_step(self) -> bool:
        """Run a single step for the given agent."""
        hider = self.board.hider
        seeker = self.board.seeker

        state_hider = self.board.get_agent_state(hider)
        state_seeker = self.board.get_agent_state(seeker)

        action_hider = self.board.get_agent_action(hider, state_hider)
        hider.position.update(action_hider)

        action_seeker = self.board.get_agent_action(seeker, state_seeker)
        seeker.position.update(action_seeker)

        new_state_hider = self.board.get_agent_state(hider)
        new_state_seeker = self.board.get_agent_state(seeker)

        reward_hider = self.board.get_agent_reward(hider)
        reward_seeker = self.board.get_agent_reward(seeker)

        self.board.update_grid()

        is_terminal, winner = self.board.is_terminal()
        if is_terminal:
            reward_hider += hider.reward_strategy.get_terminal_reward(winner)
            reward_seeker += seeker.reward_strategy.get_terminal_reward(winner)

        self.board.add_agent_transition(hider, state_hider, action_hider, reward_hider, new_state_hider, is_terminal)
        self.board.add_agent_transition(
            seeker, state_seeker, action_seeker, reward_seeker, new_state_seeker, is_terminal
        )

        self.board.update_agents()
        if self.simulation_visualizer and not is_terminal:
            self.simulation_visualizer.update(self.board)

        return is_terminal

    def _reset(self) -> None:
        self.board.reset()
