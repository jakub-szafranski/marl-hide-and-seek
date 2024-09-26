# import pytest
# from unittest.mock import Mock
# from agents.trajectory import Trajectory
# from agents.transition import Transition

# @pytest.fixture
# def trajectory():
# 	return Trajectory()

# @pytest.mark.unit
# def test_add_transition(trajectory):
# 	state = (0, 0)
# 	action = Mock()
# 	reward = 1.0
# 	next_state = (0, 1)
# 	is_terminal = False

# 	trajectory.add_transition(state, action, reward, next_state, is_terminal)
# 	assert len(trajectory.transitions) == 1
# 	assert isinstance(trajectory.transitions[0], Transition)
# 	assert trajectory.transitions[0].state == state
# 	assert trajectory.transitions[0].action == action
# 	assert trajectory.transitions[0].reward == reward
# 	assert trajectory.transitions[0].next_state == next_state
# 	assert trajectory.transitions[0].is_terminal == is_terminal

# @pytest.mark.unit
# def test_get_sub_trajectory(trajectory):
# 	for i in range(5):
# 		trajectory.add_transition((i, i), Mock(), i, (i+1, i+1), False)
	
# 	sub_trajectory = trajectory.get_sub_trajectory(3)
# 	assert len(sub_trajectory.transitions) == 3
# 	assert sub_trajectory.transitions[0].state == (2, 2)
# 	assert sub_trajectory.transitions[1].state == (3, 3)
# 	assert sub_trajectory.transitions[2].state == (4, 4)

# @pytest.mark.unit
# def test_len(trajectory):
# 	for i in range(5):
# 		trajectory.add_transition((i, i), Mock(), i, (i+1, i+1), False)
	
# 	assert len(trajectory) == 5

# @pytest.mark.unit
# def test_getitem(trajectory):
# 	for i in range(5):
# 		trajectory.add_transition((i, i), Mock(), i, (i+1, i+1), False)
	
# 	sub_trajectory = trajectory[2:]
# 	assert len(sub_trajectory.transitions) == 3
# 	assert sub_trajectory.transitions[0].state == (2, 2)
# 	assert sub_trajectory.transitions[1].state == (3, 3)
# 	assert sub_trajectory.transitions[2].state == (4, 4)