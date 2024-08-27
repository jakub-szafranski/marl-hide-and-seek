from agents.trajectory import Trajectory

from abc import ABC, abstractmethod

class LearningAlgorithm(ABC):
    def __init__(self, 
                 learning_rate: float, 
                 discount_factor: float, 
                 epsilon: float,
                 ) -> None:
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

    @abstractmethod
    def update(self, trajectory: Trajectory) -> None:
        pass

    @abstractmethod
    def get_value(self, state) -> float:
        pass

    