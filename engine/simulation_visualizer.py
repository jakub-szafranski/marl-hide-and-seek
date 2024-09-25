from __future__ import annotations
from abc import ABC, abstractmethod
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

from environment import GridCell

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Board


class SimulationVisualizer(ABC):
    @abstractmethod
    def update(self, board: Board) -> None:
        pass


class GridVisualizer(SimulationVisualizer):
    def __init__(self) -> None:
        plt.ion()
        self.fig, self.ax = plt.subplots()

    def update(self, board: Board, step_delay: float = 0.1) -> None:
        grid = board.grid
        self.ax.clear()
        cmap = ListedColormap(['white', 'blue', 'red', 'black'])
        self.ax.imshow(grid, cmap=cmap, interpolation='none')
        self.ax.set_title('Hide and Seek Simulation')

        legend_labels = {
            GridCell.EMPTY.value: 'Empty',
            GridCell.HIDER.value: 'Hider',
            GridCell.SEEKER.value: 'Seeker',
            GridCell.WALL.value: 'Wall'
        }
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cmap(i), markersize=10, label=label)
                   for i, label in legend_labels.items()]
        self.ax.legend(handles=handles, loc='upper right')

        plt.draw()
        plt.pause(step_delay)


class SimulationVisualizerFactory:
    VISUALIZERS = {GridVisualizer.__name__: GridVisualizer}

    @staticmethod
    def get_visualizer(visualizer: str) -> SimulationVisualizer:
        if visualizer not in SimulationVisualizerFactory.VISUALIZERS:
            raise ValueError(f"Visualizer {visualizer} not found")
        return SimulationVisualizerFactory.VISUALIZERS[visualizer]