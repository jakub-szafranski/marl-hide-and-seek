from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Action


@dataclass
class Transition:
    state: list
    action: Action
    reward: int
    next_state: list
    is_terminal: bool
