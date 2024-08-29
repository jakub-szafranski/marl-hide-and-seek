from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import Transition

@dataclass 
class Trajectory:
    transitions: list[Transition] = []

    def add_transition(self, transition: Transition) -> None:
        self.transitions.append(transition)

    def get_sub_trajectory(self, n: int) -> Trajectory:
        return Trajectory(self.transitions[-n:])