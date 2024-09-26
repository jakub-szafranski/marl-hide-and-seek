import pytest
from unittest.mock import Mock
from environment.reward import DurationReward, RewardFactory
from agents.agent_role import AgentRole

@pytest.fixture
def hider_reward():
    return DurationReward(agent_role=AgentRole.HIDER)

@pytest.fixture
def seeker_reward():
    return DurationReward(agent_role=AgentRole.SEEKER)

@pytest.mark.unit
def test_get_reward_hider(hider_reward):
    state = (0, 0)
    action = Mock()
    next_state = (0, 1)
    reward = hider_reward.get_reward(state, action, next_state)
    assert reward == hider_reward.STEP_REWARD_HIDER

@pytest.mark.unit
def test_get_reward_seeker(seeker_reward):
    state = (0, 0)
    action = Mock()
    next_state = (0, 1)
    reward = seeker_reward.get_reward(state, action, next_state)
    assert reward == seeker_reward.STEP_REWARD_SEEKER

@pytest.mark.unit
def test_get_terminal_reward_hider_wins(hider_reward):
    reward = hider_reward.get_terminal_reward(AgentRole.HIDER)
    assert reward == 500

@pytest.mark.unit
def test_get_terminal_reward_hider_loses(hider_reward):
    reward = hider_reward.get_terminal_reward(AgentRole.SEEKER)
    assert reward == -500

@pytest.mark.unit
def test_get_terminal_reward_seeker_wins(seeker_reward):
    reward = seeker_reward.get_terminal_reward(AgentRole.SEEKER)
    assert reward == 500

@pytest.mark.unit
def test_get_terminal_reward_seeker_loses(seeker_reward):
    reward = seeker_reward.get_terminal_reward(AgentRole.HIDER)
    assert reward == -500

@pytest.mark.unit
def test_reward_factory():
    reward_class = RewardFactory.get_reward("DurationReward")
    assert reward_class == DurationReward

    with pytest.raises(ValueError):
        RewardFactory.get_reward("NonExistentReward")