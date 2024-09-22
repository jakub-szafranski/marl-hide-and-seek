from learning import (
    LearningAlgorithm,
    Sarsa,
    QLearning,
    MonteCarlo,
)

# from .monte_carlo import MonteCarlo
# from .sarsa import Sarsa

class AlgorithmFactory:
    LEARNING_ALGORITMHS = {Sarsa.__name__: Sarsa}
    
    @staticmethod
    def get_terminal_state(terminal_state: str) -> LearningAlgorithm:
        return AlgorithmFactory.LEARNING_ALGORITMHS[terminal_state]