from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment.action import Action
    from environment.state import BaseState

@dataclass
class Transition:
    state: BaseState
    action: Action
    reward: int
    next_state: BaseState