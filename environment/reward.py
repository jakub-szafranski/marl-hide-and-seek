from abc import ABC, abstractmethod

from agents import AgentRole


class BaseReward(ABC):
    def __init__(self, agent_role: AgentRole):
        self.agent_role = agent_role

    @abstractmethod
    def get_reward(self, state, action, next_state):
        pass

    @abstractmethod
    def get_terminal_reward(self):
        pass


class DurationReward(BaseReward):
    def __init__(self, agent_role: AgentRole):
        super().__init__(agent_role)

    def get_reward(self, state, action, next_state):
        if self.agent_role == AgentRole.HIDER:
            return 1
        elif self.agent_role == AgentRole.SEEKER:
            return -1

    def get_terminal_reward(self):
        return 100
    

class RewardFactory:
    REWARDS = {DurationReward.__name__: DurationReward}

    @staticmethod
    def get_reward(reward: str) -> BaseReward:
        if reward not in RewardFactory.REWARDS:
            raise ValueError(f"Reward {reward} not found")
        return RewardFactory.REWARDS[reward]