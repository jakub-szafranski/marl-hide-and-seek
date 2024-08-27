from .trajectory import Trajectory
from .agent_position import AgentPosition
from environment.action import Action
from environment.state import BaseState
from learning.learning_algorithm import LearningAlgorithm
from action_selection.selection_algorithm import ActionSelectionStrategy

from abc import ABC, abstractmethod


class Agent(ABC):
    def __init__(self, 
                 start_position: AgentPosition, 
                 learning_algorithm: LearningAlgorithm,
                 action_selection_strategy: ActionSelectionStrategy, 
                 ) -> None:
        self.agent_position: AgentPosition = start_position
        self.learning_algorithm: LearningAlgorithm = learning_algorithm   
        self.action_selection_strategy: ActionSelectionStrategy = action_selection_strategy
        self.trajectory: Trajectory = Trajectory()

    def select_action(self, state: BaseState) -> Action:
        return self.action_selection_strategy.select_action(state, self.learning_algorithm.q_values)

    def update(self) -> None:
        self.learning_algorithm.update(self.trajectory)

    def reset(self, start_position) -> None:
        self.trajectory = Trajectory()
        self.agent_position = start_position