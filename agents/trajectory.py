from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .transition import Transition

if TYPE_CHECKING:
    from environment import Action

@dataclass
class Trajectory:
    transitions: list[Transition] = field(default_factory=list)

    def add_transition(self, state: tuple, action: Action, reward: float, next_state: tuple, is_terminal: bool,) -> None:
        transition = Transition(state, action, reward, next_state, is_terminal)
        self.transitions.append(transition)

    def get_sub_trajectory(self, n: int) -> Trajectory:
        return Trajectory(self.transitions[-n:])
    
    def __len__(self) -> int:
        return len(self.transitions)
    
    def __getitem__(self, index: int | slice) -> Trajectory:
        return Trajectory(self.transitions[index])
