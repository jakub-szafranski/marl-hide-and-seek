from enum import Enum

class GridCell(Enum):
    EMPTY = 0
    HIDER = 1
    SEEKER = 2
    WALL = 3
    SEEKER_VISION = 4
    HIDER_FOUND = 5