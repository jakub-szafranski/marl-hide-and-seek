from action_selection import ActionSelectionFactory
from engine import (Simulation, SimulationVisualizerFactory, SimulationDataCollector,)
from environment import (Board, RewardFactory, StateFactory, TerminalStateFactory,)
from learning import AlgorithmFactory
from agents import AgentRole, Agent
from utils import load_prelearned_q_values

import yaml


def main(initial_epsilon=1.0, visualize=False):
    # load pretrained q-values
    prelearned_q_values = load_prelearned_q_values('q_values.json')

    # Create the hider agent
    terminal_state = TerminalStateFactory.get_terminal_state('DetectionTerminalState')
    terminal_state = terminal_state()

    hider_action_selection = ActionSelectionFactory.get_strategy("DecayEpsilonGreedy")
    hider_action_selection = hider_action_selection(initial_epsilon=initial_epsilon, decay_rate=0.9999, min_epsilon=0.1)

    hider_learning_algorithm = AlgorithmFactory.get_algorithm("QLearning")
    hider_learning_algorithm = hider_learning_algorithm(
        learning_rate=0.05,
        discount_factor=0.99,
        default_q_value=0.0, 
    )
    if visualize:
        hider_learning_algorithm.load_prelearned_q_values(prelearned_q_values['hider_q_values'])

    hider_state_processor = StateFactory.get_hider_state('CoordinateState')
    hider_state_processor = hider_state_processor(terminal_state=terminal_state)

    hider_reward_strategy = RewardFactory.get_reward('DurationReward')
    hider_reward_strategy = hider_reward_strategy(AgentRole.HIDER)

    hider = Agent(
        agent_role=AgentRole.HIDER, 
        learning_algorithm=hider_learning_algorithm,
        action_selection_strategy=hider_action_selection,
        state_processor=hider_state_processor,
        reward_strategy=hider_reward_strategy,
        )
    
    # Create the seeker agent
    seeker_action_selection = ActionSelectionFactory.get_strategy("DecayEpsilonGreedy")
    seeker_action_selection = seeker_action_selection(initial_epsilon=initial_epsilon, decay_rate=0.9999, min_epsilon=0.1)

    seeker_learning_algorithm = AlgorithmFactory.get_algorithm("QLearning")
    seeker_learning_algorithm = seeker_learning_algorithm(
        learning_rate=0.05,
        discount_factor=0.99,
        default_q_value=0.0,
    )
    if visualize:
        seeker_learning_algorithm.load_prelearned_q_values(prelearned_q_values['seeker_q_values'])

    seeker_state_processor = StateFactory.get_seeker_state('CoordinateState')
    seeker_state_processor = seeker_state_processor(terminal_state=terminal_state)

    seeker_reward_strategy = RewardFactory.get_reward('DurationReward')
    seeker_reward_strategy = seeker_reward_strategy(AgentRole.SEEKER)

    seeker = Agent(
        agent_role=AgentRole.SEEKER, 
        learning_algorithm=seeker_learning_algorithm,
        action_selection_strategy=seeker_action_selection,
        state_processor=seeker_state_processor,
        reward_strategy=seeker_reward_strategy,
        )
    
    # Create the board
    board = Board(
        hider=hider,
        seeker=seeker,
        )
    
    # Create the simulation visualizer and data collector
    simulation_visualizer = SimulationVisualizerFactory.get_visualizer('GridVisualizer')
    simulation_visualizer = simulation_visualizer()

    simulation_data_collector = SimulationDataCollector()

    # Create the simulation
    if visualize:
        simulation = Simulation(
            board=board,
            simulation_visualizer=simulation_visualizer,
            simulation_data_collector=simulation_data_collector,
            )
    else:
        simulation = Simulation(
            board=board,
            simulation_data_collector=simulation_data_collector,
            )
    
    simulation.run()


if __name__ == "__main__":
    # main(initial_epsilon=0.001, visualize=True)
    main(initial_epsilon=1.0, visualize=False)
