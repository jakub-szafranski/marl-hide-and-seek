from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from agents.transition import Transition

if TYPE_CHECKING:
    from environment import Action

@dataclass
class Trajectory:
    transitions: list[Transition] = field(default_factory=list)

    def add_transition(self, state: list, action: Action, reward: float, next_state: list, is_terminal: bool,) -> None:
        transition = Transition(state, action, reward, next_state, is_terminal)
        self.transitions.append(transition)

    def get_sub_trajectory(self, n: int) -> Trajectory:
        return Trajectory(self.transitions[-n:])
