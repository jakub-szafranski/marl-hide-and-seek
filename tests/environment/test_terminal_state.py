import pytest
from unittest.mock import Mock
from environment.terminal_state import DetectionTerminalState, TerminalStateFactory
from agents.agent_role import AgentRole

@pytest.fixture
def board():
    mock_board = Mock()
    mock_board.hider.position.x = 1
    mock_board.hider.position.y = 2
    mock_board.seeker.position.x = 1
    mock_board.seeker.position.y = 2
    mock_board.seeker.trajectory = [(0, 0), (1, 1)]
    return mock_board

@pytest.fixture
def detection_terminal_state():
    detection_terminal_state = DetectionTerminalState()
    detection_terminal_state.detection_distance = 1
    detection_terminal_state.max_steps = 10
    return detection_terminal_state

@pytest.mark.unit
def test_is_terminal_detection(detection_terminal_state, board):
    is_terminal, winner = detection_terminal_state.is_terminal(board)
    assert is_terminal is True
    assert winner == AgentRole.SEEKER

@pytest.mark.unit
def test_is_terminal_max_steps(detection_terminal_state, board):
    board.seeker.trajectory = [(0, 0)] * 10
    board.seeker.position.x = 0
    board.seeker.position.y = 0
    board.hider.position.x = 0
    board.hider.position.y = 4
    
    is_terminal, winner = detection_terminal_state.is_terminal(board)
    assert is_terminal is True
    assert winner == AgentRole.HIDER

@pytest.mark.unit
def test_terminal_state_factory():
    terminal_state_class = TerminalStateFactory.get_terminal_state("DetectionTerminalState")
    assert terminal_state_class == DetectionTerminalState

    with pytest.raises(ValueError):
        TerminalStateFactory.get_terminal_state("NonExistentTerminalState")