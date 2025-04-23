from __future__ import annotations
from typing import TYPE_CHECKING

from enum import Enum, auto
from dataclasses import dataclass, field
import yaml

from src.agents.action import Action

if TYPE_CHECKING:
    from src.agents import AgentPosition, LearningAlgorithm, ActionSelectionStrategy, BaseState, BaseReward


class AgentRole(Enum):
    HIDER = auto()
    SEEKER = auto()


@dataclass
class AgentPosition:
    x: int
    y: int

    def __post_init__(self):
        with open("config.yml", "r") as file:
            self.config = yaml.safe_load(file)
        self.walls = self.config.get("walls", [])

    def update(self, action: Action) -> None:
        new_x, new_y = self.x, self.y

        if action == Action.UP:
            new_y = min(self.y + 1, self.config["grid_height"] - 1)
        elif action == Action.DOWN:
            new_y = max(self.y - 1, 0)
        elif action == Action.LEFT:
            new_x = max(self.x - 1, 0)
        elif action == Action.RIGHT:
            new_x = min(self.x + 1, self.config["grid_width"] - 1)
        elif action == Action.STAY:
            new_x, new_y = self.x, self.y

        if [new_x, new_y] not in self.walls:
            self.x, self.y = new_x, new_y


@dataclass
class Transition:
    state: tuple
    action: Action
    reward: int
    next_state: tuple
    is_terminal: bool

    def __iter__(self) -> iter[tuple, Action, int, tuple, bool]:
        return iter((self.state, self.action, self.reward, self.next_state, self.is_terminal))


@dataclass
class Trajectory:
    transitions: list[Transition] = field(default_factory=list)

    def add_transition(
        self,
        state: tuple,
        action: Action,
        reward: float,
        next_state: tuple,
        is_terminal: bool,
    ) -> None:
        transition = Transition(state, action, reward, next_state, is_terminal)
        self.transitions.append(transition)

    def get_sub_trajectory(self, n: int) -> Trajectory:
        return Trajectory(self.transitions[-n:])

    def __len__(self) -> int:
        return len(self.transitions)

    def __getitem__(self, index: int | slice) -> Trajectory:
        return Trajectory(self.transitions[index])


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
        return self.action_selection_strategy.select_action(state, self.learning_algorithm.q_values)

    def update(self) -> None:
        self.learning_algorithm.update(self.trajectory)

    def reset(self) -> None:
        self.trajectory = Trajectory()
        self.position = None
