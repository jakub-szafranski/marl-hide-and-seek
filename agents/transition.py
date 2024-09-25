from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Action


@dataclass
class Transition:
    state: tuple
    action: Action
    reward: int
    next_state: tuple
    is_terminal: bool

    def __iter__(self) -> iter[tuple, Action, int, tuple, bool]:
        return iter((self.state, self.action, self.reward, self.next_state, self.is_terminal))
