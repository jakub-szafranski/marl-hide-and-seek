import random
import yaml
import json
from collections import defaultdict
import matplotlib.pyplot as plt

from agents import AgentPosition, Trajectory, Agent
from environment import Action


def generate_start_coordinates() -> tuple[AgentPosition, AgentPosition]:
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)

    grid_height = config["grid_height"]
    grid_width = config["grid_width"]
    detection_distance = config["detection_distance"]
    wall_positions = config["walls"]

    while True:
        hider_x = random.randint(0, grid_width - 1)
        hider_y = random.randint(0, grid_height - 1)

        seeker_x = random.randint(0, grid_width - 1)
        seeker_y = random.randint(0, grid_height - 1)

        if (
            [hider_x, hider_y] not in wall_positions
            and [seeker_x, seeker_y] not in wall_positions
            and abs(hider_x - seeker_x) > detection_distance
            and abs(hider_y - seeker_y) > detection_distance
        ):
            return AgentPosition(hider_x, hider_y), AgentPosition(seeker_x, seeker_y)

def calculate_episode_return(trajectory: Trajectory) -> float:
    return sum(transition.reward for transition in trajectory.transitions)

def json_serializable_q_values(q_values: defaultdict) -> dict:
    return {str(k): {action.value: v for action, v in actions.items()} for k, actions in q_values.items()}

def load_prelearned_q_values(file_path: str) -> dict:
    with open(file_path, "r") as file:
        prelearned_q_values = json.load(file)
    
    prelearned_q_values["hider_q_values"] = {eval(k): {Action(int(action)): v for action, v in actions.items()} for k, actions in prelearned_q_values["hider_q_values"].items()}
    prelearned_q_values["seeker_q_values"] = {eval(k): {Action(int(action)): v for action, v in actions.items()} for k, actions in prelearned_q_values["seeker_q_values"].items()}

    return prelearned_q_values


    @staticmethod
    def _is_line_blocked(start, end, wall_positions):
        """Check if the line from start to end is blocked by any wall."""
        x0, y0 = start
        x1, y1 = end
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            if [x0, y0] in wall_positions:
                return True
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return False

    @staticmethod
    def _process_seeker_vision(seeker: Agent, wall_positions: list, vision_distance: int) -> list:
        visible_cells = []
        seeker_x = seeker.position.x
        seeker_y = seeker.position.y
        for dx in range(-vision_distance, vision_distance + 1):
            for dy in range(-vision_distance, vision_distance + 1):
                x, y = seeker_x + dx, seeker_y + dy
                if not BoardBuilder._is_line_blocked((seeker_x, seeker_y), (x, y), wall_positions):
                    visible_cells.append([x, y])
        return visible_cells