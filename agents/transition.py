from environment.state import BaseState
from environment.action import Action

from dataclasses import dataclass

@dataclass
class Transition:
    state: BaseState
    action: Action
    reward: int
    next_state: BaseState