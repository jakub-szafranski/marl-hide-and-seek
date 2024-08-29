import random
import yaml
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agents import AgentPosition


def generate_start_coordinates() -> tuple[AgentPosition, AgentPosition]:
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

    grid_height = config['grid_height']
    grid_width = config['grid_width']
    detection_distance = config['detection_distance']
    wall_positions = config['wall_positions']

    while True:
        hider_x = random.randint(0, grid_width - 1)
        hider_y = random.randint(0, grid_height - 1)

        seeker_x = random.randint(0, grid_width - 1)
        seeker_y = random.randint(0, grid_height - 1)

        if (hider_x, hider_y) not in wall_positions and (seeker_x, seeker_y) not in wall_positions and abs(hider_x - seeker_x) + abs(hider_y - seeker_y) > detection_distance:
            return AgentPosition(hider_x, hider_y), AgentPosition(seeker_x, seeker_y)


    

