# import pytest
# from unittest.mock import Mock
# from agents.agent import Agent
# from agents.trajectory import Trajectory

# @pytest.fixture
# def agent_role():
#     return Mock()

# @pytest.fixture
# def learning_algorithm():
#     mock = Mock()
#     mock.q_values = {}
#     return mock

# @pytest.fixture
# def action_selection_strategy():
#     mock = Mock()
#     mock.select_action = Mock(return_value="mock_action")
#     return mock

# @pytest.fixture
# def state_processor():
#     return Mock()

# @pytest.fixture
# def reward_strategy():
#     return Mock()

# @pytest.fixture
# def start_position():
#     return Mock()

# @pytest.fixture
# def agent(agent_role, learning_algorithm, action_selection_strategy, state_processor, reward_strategy, start_position):
#     return Agent(
#         agent_role=agent_role,
#         learning_algorithm=learning_algorithm,
#         action_selection_strategy=action_selection_strategy,
#         state_processor=state_processor,
#         reward_strategy=reward_strategy,
#         start_position=start_position
#     )

# @pytest.mark.unit
# def test_select_action(agent):
#     state = Mock()
#     action = agent.select_action(state)
#     agent.action_selection_strategy.select_action.assert_called_once_with(state, agent.learning_algorithm.q_values)
#     assert action == "mock_action"

# @pytest.mark.unit
# def test_update(agent):
#     agent.update()
#     agent.learning_algorithm.update.assert_called_once_with(agent.trajectory)

# @pytest.mark.unit
# def test_reset(agent):
#     agent.reset()
#     assert isinstance(agent.trajectory, Trajectory)
#     assert agent.position is None