from __future__ import annotations
from abc import ABC, abstractmethod
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np

from environment import GridCell
from agents import AgentRole

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from environment import Board


class SimulationVisualizer(ABC):
    @abstractmethod
    def update(self, board: Board) -> None:
        pass


class GridVisualizer(SimulationVisualizer):
    def __init__(self, step_delay: float = 0.1, terminal_delay: float = 2) -> None:
        self.step_delay = step_delay
        self.terminal_delay = terminal_delay

        plt.ion()
        self.fig, self.ax = plt.subplots()

    def update(self, board: Board) -> None:
        grid = board.grid
        is_terminal, winner = board.is_terminal()

        self.ax.clear()
        cmap = ListedColormap(['white', 'blue', 'red', 'black'])

        self.ax.imshow(grid == GridCell.WALL.value, cmap=ListedColormap(['white', 'black']), interpolation='none')

        if winner == AgentRole.SEEKER:
            hider_positions = np.argwhere(grid == GridCell.HIDER_FOUND.value)
        else:
            hider_positions = np.argwhere(grid == GridCell.HIDER.value)
        seeker_positions = np.argwhere(grid == GridCell.SEEKER.value)
        seeker_vision_positions = np.argwhere(grid == GridCell.SEEKER_VISION.value)

        for pos in seeker_vision_positions:
            rect = plt.Rectangle((pos[1] - 0.5, pos[0] - 0.5), 1, 1, color='red', alpha=0.3, linewidth=0)
            self.ax.add_patch(rect)

        for pos in seeker_positions:
            rect = plt.Rectangle((pos[1] - 0.5, pos[0] - 0.5), 1, 1, color='red', alpha=0.3, linewidth=0)
            self.ax.add_patch(rect)

        if is_terminal:
            color = 'green' if winner == AgentRole.HIDER else 'red'
            for pos in hider_positions:
                rect = plt.Rectangle((pos[1] - 0.5, pos[0] - 0.5), 1, 1, color=color, alpha=0.6, linewidth=0)
                self.ax.add_patch(rect)

        self.ax.scatter(hider_positions[:, 1], hider_positions[:, 0], color='blue', label='Hider', s=300)
        self.ax.scatter(seeker_positions[:, 1], seeker_positions[:, 0], color='red', label='Seeker', s=300)

        self.ax.set_title('Hide and Seek Simulation')

        legend_labels = {
            GridCell.HIDER.value: 'Hider',
            GridCell.SEEKER.value: 'Seeker',
            GridCell.WALL.value: 'Wall',
        }
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cmap(i), markersize=10, label=label)
                   for i, label in legend_labels.items()]
        self.ax.legend(handles=handles, loc='upper right')
        
        plt.draw()
        if is_terminal:
            plt.pause(self.terminal_delay)
        plt.pause(self.step_delay)


class SimulationVisualizerFactory:
    VISUALIZERS = {GridVisualizer.__name__: GridVisualizer}

    @staticmethod
    def get_visualizer(visualizer: str) -> SimulationVisualizer:
        if visualizer not in SimulationVisualizerFactory.VISUALIZERS:
            raise ValueError(f"Visualizer {visualizer} not found")
        return SimulationVisualizerFactory.VISUALIZERS[visualizer]