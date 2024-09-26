import pytest
from unittest.mock import mock_open, patch
from environment.action import Action
from agents.agent_position import AgentPosition

@pytest.fixture
def agent_position():
    with patch("builtins.open", mock_open(read_data="""
    grid_height: 5
    grid_width: 5
    walls:
      - [1, 1]
      - [2, 2]
    """)):
        return AgentPosition(x=0, y=0)

@pytest.mark.unit
def test_update_position(agent_position):
    agent_position.update(Action.UP)
    assert agent_position.x == 0
    assert agent_position.y == 1

    agent_position.update(Action.RIGHT)
    assert agent_position.x == 0
    assert agent_position.y == 1

    agent_position.update(Action.DOWN)
    assert agent_position.x == 0
    assert agent_position.y == 0

    agent_position.update(Action.LEFT)
    assert agent_position.x == 0
    assert agent_position.y == 0

@pytest.mark.unit
def test_update_position_with_walls(agent_position):
    agent_position.update(Action.UP)
    agent_position.update(Action.RIGHT)
    agent_position.update(Action.RIGHT)
    assert agent_position.x == 0
    assert agent_position.y == 1 

    agent_position.update(Action.UP)
    assert agent_position.x == 0
    assert agent_position.y == 2

    agent_position.update(Action.LEFT)
    assert agent_position.x == 0 
    assert agent_position.y == 2