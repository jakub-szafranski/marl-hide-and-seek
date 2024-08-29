from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import AgentPosition, Trajectory, AgentRole
    from environment import Action, BaseState
    from learning import LearningAlgorithm
    from action_selection import ActionSelectionStrategy


class Agent:
    def __init__(
        self,
        agent_role: AgentRole,
        learning_algorithm: LearningAlgorithm,
        action_selection_strategy: ActionSelectionStrategy,
        start_position: AgentPosition = None,
    ) -> None:
        self.agent_role = agent_role
        self.position = start_position
        self.learning_algorithm = learning_algorithm
        self.action_selection_strategy = action_selection_strategy
        self.trajectory = Trajectory()

    def select_action(self, state: BaseState) -> Action:
        return self.action_selection_strategy.select_action(
            state, self.learning_algorithm.q_values # q_values or get_value?
        )

    def update(self) -> None:
        self.learning_algorithm.update(self.trajectory)

    def reset(self) -> None:
        self.trajectory = Trajectory()
        self.position = None
