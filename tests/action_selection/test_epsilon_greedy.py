import pytest
import random
from collections import defaultdict
from action_selection import EpsilonGreedy
from environment import Action

@pytest.fixture
def epsilon_greedy():
    return EpsilonGreedy(epsilon=0.1)

@pytest.fixture
def q_values():
    q = defaultdict(lambda: defaultdict(float))
    state = "dummy_state"
    q[state][Action.UP] = 1.0
    q[state][Action.DOWN] = 2.0
    q[state][Action.RIGHT] = 3.0
    return q

@pytest.mark.unit
def test_select_action_random(epsilon_greedy, q_values, monkeypatch):
    state = "dummy_state"
    
    def mock_random():
        return 0.05  # Less than epsilon to force random action selection
    
    monkeypatch.setattr(random, 'random', mock_random)
    
    action = epsilon_greedy.select_action(state, q_values)
    assert action in list(Action)

@pytest.mark.unit
def test_select_action_best(epsilon_greedy, q_values, monkeypatch):
    state = "dummy_state"
    
    def mock_random():
        return 0.2  # Greater than epsilon to force best action selection
    
    monkeypatch.setattr(random, 'random', mock_random)
    
    action = epsilon_greedy.select_action(state, q_values)
    assert action == Action.RIGHT