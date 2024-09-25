from __future__ import annotations
from typing import TYPE_CHECKING

from .trajectory import Trajectory

if TYPE_CHECKING:
    from agents import AgentPosition, AgentRole
    from environment import Action, BaseState, BaseReward
    from learning import LearningAlgorithm
    from action_selection import ActionSelectionStrategy


class Agent:
    def __init__(
        self,
        agent_role: AgentRole,
        learning_algorithm: LearningAlgorithm,
        action_selection_strategy: ActionSelectionStrategy,
        state_processor: BaseState,
        reward_strategy: BaseReward,
        start_position: AgentPosition = None,
    ) -> None:
        self.agent_role = agent_role
        self.learning_algorithm = learning_algorithm
        self.action_selection_strategy = action_selection_strategy
        self.state_processor = state_processor
        self.reward_strategy = reward_strategy
        self.position = start_position
        self.trajectory = Trajectory()

    def select_action(self, state: BaseState) -> Action:
        return self.action_selection_strategy.select_action(
            state, self.learning_algorithm.q_values
        )

    def update(self) -> None:
        self.learning_algorithm.update(self.trajectory)

    def reset(self) -> None:
        self.trajectory = Trajectory()
        self.position = None
