from learning import (
    LearningAlgorithm,
    Sarsa,
    QLearning,
    MonteCarlo,
)


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
        return AlgorithmFactory.LEARNING_ALGORITMHS[algorithm]
