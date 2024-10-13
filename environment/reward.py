from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from agents import AgentRole

if TYPE_CHECKING:
    from environment import Action


class BaseReward(ABC):
    def __init__(self, agent_role: AgentRole):
        self.agent_role = agent_role

    @abstractmethod
    def get_reward(self, state: tuple, action: Action, next_state: tuple) -> float:
        pass


class DurationReward(BaseReward):
    STEP_REWARD_HIDER = 1
    STEP_REWARD_SEEKER = -1
    TERMINAL_REWARD = 50

    def __init__(self, agent_role: AgentRole):
        super().__init__(agent_role)

    def get_reward(self, state: tuple, action: Action, next_state: tuple) -> float:            
        if self.agent_role == AgentRole.HIDER:
            return self.STEP_REWARD_HIDER
        elif self.agent_role == AgentRole.SEEKER:
            return self.STEP_REWARD_SEEKER

    def get_terminal_reward(self, winner: AgentRole) -> float:
        if self.agent_role == winner:
            return self.TERMINAL_REWARD
        else:
            return -self.TERMINAL_REWARD
    

class WinLoseReward(BaseReward):
    TERMINAL_REWARD = 50

    def __init__(self, agent_role: AgentRole):
        super().__init__(agent_role)

    def get_reward(self, state: tuple, action: Action, next_state: tuple) -> float:            
        return 0

    def get_terminal_reward(self, winner: AgentRole) -> float:
        if self.agent_role == winner:
            return self.TERMINAL_REWARD
        else:
            return -self.TERMINAL_REWARD


class RewardFactory:
    REWARDS = {DurationReward.__name__: DurationReward}

    @staticmethod
    def get_reward(reward: str) -> BaseReward:
        if reward not in RewardFactory.REWARDS:
            raise ValueError(f"Reward {reward} not found")
        return RewardFactory.REWARDS[reward]