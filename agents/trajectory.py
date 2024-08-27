from .transition import Transition

from dataclasses import dataclass
from __future__ import annotations


@dataclass 
class Trajectory:
    transitions: list[Transition] = []

    def add_transition(self, transition: Transition) -> None:
        self.transitions.append(transition)

    def get_sub_trajectory(self, n: int) -> Trajectory:
        return Trajectory(self.transitions[-n:])