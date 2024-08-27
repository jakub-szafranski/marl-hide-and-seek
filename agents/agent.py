from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents.agent import AgentPosition, Trajectory
    from environment.action import Action
    from environment.state import BaseState
    from learning.learning_algorithm import LearningAlgorithm
    from action_selection.action_selection_strategy import ActionSelectionStrategy

class Agent:
    def __init__(self, 
                 start_position: AgentPosition, 
                 learning_algorithm: LearningAlgorithm,
                 action_selection_strategy: ActionSelectionStrategy, 
                 ) -> None:
        self.agent_position = start_position
        self.learning_algorithm = learning_algorithm   
        self.action_selection_strategy = action_selection_strategy
        self.trajectory = Trajectory()

    def select_action(self, state: BaseState) -> Action:
        return self.action_selection_strategy.select_action(state, self.learning_algorithm.q_values)

    def update(self) -> None:
        self.learning_algorithm.update(self.trajectory)

    def reset(self, start_position: AgentPosition) -> None:
        self.trajectory = Trajectory()
        self.agent_position = start_position