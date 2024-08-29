import yaml
from typing import TYPE_CHECKING

from utils import generate_start_coordinates
# TODO imports, implementations, and method calls are missing

if TYPE_CHECKING:
    from agents import Agent
    from environment import Board, TerminalState, BaseState, BaseReward


class Simulation:
    def __init__(
        self,
        board: Board,
        hider_state_processor: BaseState,
        seeker_state_processor: BaseState,
        hider_reward_strategy: BaseReward,
        seeker_reward_strategy: BaseReward,
    ) -> None:
        self.board = board
        self.hider_state_processor = hider_state_processor
        self.seeker_state_processor = seeker_state_processor
        self.hider_reward_strategy = hider_reward_strategy
        self.seeker_reward_strategy = seeker_reward_strategy

    def run(self) -> None:
        total_episodes = self.config["total_episodes"]
        for episode in range(total_episodes):
            # TODO: add logging there
            self._run_episode()
            self._reset()

    def _run_episode(self) -> None:
        """Run a single episode of the simulation."""
        episode_finished = False
        while not episode_finished:
            episode_finished = self._run_step()

    def _run_step(self) -> bool:
        """Run a single step for the given agent."""
        state_hider = self.hider_state_processor.get_state(self.board)
        state_seeker = self.seeker_state_processor.get_state(self.board)

        action_hider = self.board.hider.select_action(state_hider)
        self.board.hider.position.update(action_hider)

        action_seeker = self.board.seeker.select_action(state_seeker)
        self.board.seeker.position.update(action_seeker)

        new_state_hider = self.hider_state_processor.get_state(self.board)
        new_state_seeker = self.seeker_state_processor.get_state(self.board)

        reward_hider = self.hider_reward_strategy.get_reward(state_hider, action_hider, new_state_hider)
        reward_seeker = self.seeker_reward_strategy.get_reward(state_seeker, action_seeker, new_state_seeker)

        is_terminal = self.seeker_state_processor.is_terminal(self.board)
        self.board.hider.trajectory.add_transition(state_hider, action_hider, reward_hider, new_state_hider, is_terminal)
        self.board.seeker.trajectory.add_transition(state_seeker, action_seeker, reward_seeker, new_state_seeker, is_terminal)

        self.board.hider.update()
        self.board.seeker.update()
        self.board.update_grid()

        return is_terminal  

    def _reset(self) -> None:
        self.board.reset()
