from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.agents import AgentRole

if TYPE_CHECKING:
    from src.agents.action import Action


class BaseReward(ABC):
    def __init__(self, agent_role: AgentRole):
        self.agent_role = agent_role

    @abstractmethod
    def get_reward(self, *args, **kwargs) -> float:
        """
        Function to calculate the reward for the agent.
        """
        pass

    def get_terminal_reward(self, winner: AgentRole) -> float:
        if self.agent_role == winner:
            return self.TERMINAL_REWARD
        else:
            return -self.TERMINAL_REWARD


class DurationReward(BaseReward):
    STEP_REWARD_HIDER = 1
    STEP_REWARD_SEEKER = -1
    TERMINAL_REWARD = 50

    def __init__(self, agent_role: AgentRole):
        super().__init__(agent_role)

    def get_reward(self) -> float:
        if self.agent_role == AgentRole.HIDER:
            return self.STEP_REWARD_HIDER
        elif self.agent_role == AgentRole.SEEKER:
            return self.STEP_REWARD_SEEKER


class WinLoseReward(BaseReward):
    TERMINAL_REWARD = 50

    def __init__(self, agent_role: AgentRole):
        super().__init__(agent_role)

    def get_reward(self) -> float:
        return 0


class RewardFactory:
    REWARDS = {
        DurationReward.__name__: DurationReward,
        WinLoseReward.__name__: WinLoseReward,
    }

    @staticmethod
    def get_reward(reward: str) -> BaseReward:
        if reward not in RewardFactory.REWARDS:
            raise ValueError(f"Reward {reward} not found")
        return RewardFactory.REWARDS[reward]
