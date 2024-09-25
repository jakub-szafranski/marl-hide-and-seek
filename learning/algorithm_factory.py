from .sarsa import Sarsa
from .q_learning import QLearning
from .monte_carlo import MonteCarlo
from .learning_algorithm import LearningAlgorithm


class AlgorithmFactory:
    LEARNING_ALGORITHMS = {
        Sarsa.__name__: Sarsa,
        QLearning.__name__: QLearning,
        MonteCarlo.__name__: MonteCarlo
        }
    
    @staticmethod
    def get_algorithm(algorithm: str) -> LearningAlgorithm:
        if algorithm not in AlgorithmFactory.LEARNING_ALGORITHMS:
            raise ValueError(f"Algorithm {algorithm} not found")
        return AlgorithmFactory.LEARNING_ALGORITHMS[algorithm]
