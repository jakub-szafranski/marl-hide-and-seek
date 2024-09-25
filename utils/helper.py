import random
import yaml
import json
from collections import defaultdict

from agents import AgentPosition, Trajectory
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
            (hider_x, hider_y) not in wall_positions
            and (seeker_x, seeker_y) not in wall_positions
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