import pytest
from unittest.mock import Mock
from environment.state import CoordinateState, StateFactory
from agents.agent_role import AgentRole

@pytest.fixture
def terminal_state():
    return Mock()

@pytest.fixture
def board():
    mock_board = Mock()
    mock_board.seeker.trajectory = [1]
    mock_board.hider.position.x = 1
    mock_board.hider.position.y = 2
    mock_board.seeker.position.x = 3
    mock_board.seeker.position.y = 4
    return mock_board

@pytest.fixture
def coordinate_state(terminal_state):
    return CoordinateState(terminal_state)

@pytest.mark.unit
def test_get_state(coordinate_state, board):
    state = coordinate_state.get_state(board)
    assert state == (1, 2, 3, 4, 1)

@pytest.mark.unit
def test_is_terminal(coordinate_state, board, terminal_state):
    terminal_state.is_terminal.return_value = (True, AgentRole.HIDER)
    is_terminal, winner = coordinate_state.is_terminal(board)
    assert is_terminal is True
    assert winner == AgentRole.HIDER

@pytest.mark.unit
def test_state_factory_get_seeker_state():
    state_class = StateFactory.get_seeker_state("CoordinateState")
    assert state_class == CoordinateState

    with pytest.raises(ValueError):
        StateFactory.get_seeker_state("NonExistentState")

@pytest.mark.unit
def test_state_factory_get_hider_state():
    state_class = StateFactory.get_hider_state("CoordinateState")
    assert state_class == CoordinateState

    with pytest.raises(ValueError):
        StateFactory.get_hider_state("NonExistentState")