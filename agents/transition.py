from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Action, BaseState

@dataclass
class Transition:
    state: BaseState
    action: Action
    reward: int
    next_state: BaseState