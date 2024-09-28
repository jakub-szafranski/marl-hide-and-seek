import pytest
from unittest.mock import Mock
from learning import Sarsa
from agents import Trajectory, Transition
from environment import Action

@pytest.fixture
def sarsa_n1():
    return Sarsa(learning_rate=0.1, discount_factor=0.9, default_q_value=1.0, n_steps=1)

@pytest.fixture
def sarsa_n2():
    return Sarsa(learning_rate=0.1, discount_factor=0.9, default_q_value=1.0, n_steps=2)

@pytest.fixture
def trajectory():
    state1 = "dummy_state1"
    state2 = "dummy_state2"
    state3 = "dummy_state3"
    action1 = Mock(spec=Action)
    action2 = Mock(spec=Action)
    action3 = Mock(spec=Action)
    transition1 = Transition(state=state1, action=action1, reward=1, next_state=state2, is_terminal=False)
    transition2 = Transition(state=state2, action=action2, reward=2, next_state=state3, is_terminal=False)
    transition3 = Transition(state=state3, action=action3, reward=3, next_state=None, is_terminal=False)
    return Trajectory(transitions=[transition1, transition2, transition3])

@pytest.mark.unit
def test_update_n_step_1(sarsa_n1, trajectory):
    expected_q_value = 1.0 + 0.1 * (2 + 0.9 * 1.0 - 1.0)  # current_q_value + learning_rate * (reward + discount_factor * next_q_value - current_q_value)
    
    sarsa_n1.update(trajectory)
    
    updated_q_value = sarsa_n1.q_values[trajectory.transitions[-2].state][trajectory.transitions[-2].action]
    assert updated_q_value == pytest.approx(expected_q_value, abs=1e-6)

@pytest.mark.unit
def test_update_n_step_2(sarsa_n2, trajectory):
    expected_q_value = 1.0 + 0.1 * (1 + 0.9 * 2 + 0.9**2 * 1 - 1.0)  # current_q_value + learning_rate * (sum of discounted rewards + discounted next_q_value - current_q_value)
    
    sarsa_n2.update(trajectory)
    
    updated_q_value = sarsa_n2.q_values[trajectory.transitions[0].state][trajectory.transitions[0].action]
    assert updated_q_value == pytest.approx(expected_q_value, abs=1e-6)

@pytest.mark.unit
def test_update_terminal_state_n_step_2(sarsa_n2, trajectory):
    # For terminal state, the next state Q-value should not be added
    expected_q_value_s1 = 1.0 + 0.1 * (1 + 0.9 * 2 + 0.9**2 * 3 - 1.0)  # current_q_value + learning_rate * (sum of discounted rewards - current_q_value)
    expected_q_value_s2 = 1.0 + 0.1 * (2 + 0.9 * 3 - 1.0)
    expected_q_value_s3 = 1.0 + 0.1 * (3 - 1.0)

    # Modify trajectory to end in terminal state
    trajectory.transitions[-1].is_terminal = True
    
    sarsa_n2.update(trajectory)
    
    updated_q_value = sarsa_n2.q_values[trajectory.transitions[0].state][trajectory.transitions[0].action]
    assert updated_q_value == pytest.approx(expected_q_value_s1, abs=1e-6)

    updated_q_value = sarsa_n2.q_values[trajectory.transitions[1].state][trajectory.transitions[1].action]
    assert updated_q_value == pytest.approx(expected_q_value_s2, abs=1e-6)

    updated_q_value = sarsa_n2.q_values[trajectory.transitions[2].state][trajectory.transitions[2].action]
    assert updated_q_value == pytest.approx(expected_q_value_s3, abs=1e-6)