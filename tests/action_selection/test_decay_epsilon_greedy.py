import pytest
import random
from collections import defaultdict
from action_selection import DecayEpsilonGreedy
from environment import Action

@pytest.fixture
def decay_epsilon_greedy():
    return DecayEpsilonGreedy(initial_epsilon=0.1, decay_rate=0.9, min_epsilon=0.01)

@pytest.fixture
def q_values():
    q = defaultdict(lambda: defaultdict(float))
    state = "dummy_state"
    q[state][Action.UP] = 1.0
    q[state][Action.DOWN] = 2.0
    q[state][Action.RIGHT] = 3.0
    return q

@pytest.mark.unit
def test_select_action_random(decay_epsilon_greedy, q_values, monkeypatch):
    state = "dummy_state"
    
    def mock_random():
        return 0.05  # Less than epsilon to force random action selection
    
    monkeypatch.setattr(random, 'random', mock_random)
    
    action = decay_epsilon_greedy.select_action(state, q_values)
    assert action in list(Action)

@pytest.mark.unit
def test_select_action_best(decay_epsilon_greedy, q_values, monkeypatch):
    state = "dummy_state"
    
    def mock_random():
        return 0.2  # Greater than epsilon to force best action selection
    
    monkeypatch.setattr(random, 'random', mock_random)
    
    action = decay_epsilon_greedy.select_action(state, q_values)
    assert action == Action.RIGHT

@pytest.mark.unit
def test_epsilon_decay(decay_epsilon_greedy, q_values, monkeypatch):
    state = "dummy_state"
    
    def mock_random():
        return 0.2  # Greater than epsilon to force best action selection
    
    monkeypatch.setattr(random, 'random', mock_random)
    
    initial_epsilon = decay_epsilon_greedy.epsilon
    decay_epsilon_greedy.select_action(state, q_values)

    expected_epsilon = initial_epsilon * decay_epsilon_greedy.decay_rate
    assert decay_epsilon_greedy.epsilon == pytest.approx(expected_epsilon, abs=1e-6)