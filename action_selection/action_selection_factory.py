from .epsilon_greedy import EpsilonGreedy
from .decay_epsilon_greedy import DecayEpsilonGreedy

class ActionSelectionFactory:
    ACTION_SELECTION_STRATEGIES = {
        EpsilonGreedy.__name__: EpsilonGreedy,
        DecayEpsilonGreedy.__name__: DecayEpsilonGreedy,
    }

    @staticmethod
    def get_strategy(action_selection: str):
        if action_selection not in ActionSelectionFactory.ACTION_SELECTION_STRATEGIES:
            raise ValueError(f"Action selection {action_selection} not found")
        return ActionSelectionFactory.ACTION_SELECTION_STRATEGIES[action_selection]