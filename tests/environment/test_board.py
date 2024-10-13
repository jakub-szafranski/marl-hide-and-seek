import pytest
from unittest.mock import Mock, patch, mock_open
import yaml
from environment.board.board import Board


@pytest.fixture
def config():
    return {
        "grid_height": 10,
        "grid_width": 10,
        "detection_distance": 1,
        "walls": [[1, 1], [2, 2]]
    }

@pytest.fixture
def hider():
    mock = Mock()
    mock.position = Mock(x=0, y=0)
    return mock

@pytest.fixture
def seeker():
    mock = Mock()
    mock.position = Mock(x=4, y=4)
    return mock

@pytest.fixture
def board(hider, seeker, config):
    with patch("builtins.open", mock_open(read_data=yaml.dump(config))):
        return Board(hider=hider, seeker=seeker)

@pytest.mark.unit
def test_board_initialization(board, config):
    assert board.config == config
    assert board.grid.shape == (config["grid_height"], config["grid_width"])

@pytest.mark.unit
def test_get_agent_state(board):
    agent = Mock()
    state = board.get_agent_state(agent)
    agent.state_processor.get_state.assert_called_once_with(board)
    assert state == agent.state_processor.get_state.return_value

@pytest.mark.unit
def test_get_agent_action(board):
    agent = Mock()
    state = Mock()
    action = board.get_agent_action(agent, state)
    agent.select_action.assert_called_once_with(state)
    assert action == agent.select_action.return_value

@pytest.mark.unit
def test_get_agent_reward(board):
    agent = Mock()
    state = Mock()
    action = Mock()
    new_state = Mock()
    reward = board.get_agent_reward(agent, state, action, new_state)
    agent.reward_strategy.get_reward.assert_called_once_with(state, action, new_state)
    assert reward == agent.reward_strategy.get_reward.return_value

@pytest.mark.unit
def test_is_terminal(board):
    board.hider.state_processor.is_terminal.return_value = (False, None)
    board.seeker.state_processor.is_terminal.return_value = (True, Mock())
    is_terminal, winner = board.is_terminal()
    assert is_terminal is True

@pytest.mark.unit
def test_add_agent_transition(board):
    agent = Mock()
    state = Mock()
    action = Mock()
    reward = Mock()
    new_state = Mock()
    is_terminal = Mock()
    board.add_agent_transition(agent, state, action, reward, new_state, is_terminal)
    agent.trajectory.add_transition.assert_called_once_with(state, action, reward, new_state, is_terminal)

@pytest.mark.unit
def test_update(board):
    board.update()
    board.hider.update.assert_called_once()
    board.seeker.update.assert_called_once()
    assert board.grid.shape == (board.config["grid_height"], board.config["grid_width"])

@pytest.mark.unit
def test_reset(board):
    board.reset()
    board.hider.reset.assert_called_once()
    board.seeker.reset.assert_called_once()
    assert board.grid.shape == (board.config["grid_height"], board.config["grid_width"])