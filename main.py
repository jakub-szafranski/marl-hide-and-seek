from action_selection import ActionSelectionFactory
from engine import (Simulation, SimulationVisualizerFactory,)
from environment import (Board, RewardFactory, StateFactory, TerminalStateFactory,)
from learning import AlgorithmFactory
from agents import AgentRole, Agent


def main():
    # Create the hider agent
    terminal_state = TerminalStateFactory.get_terminal_state('DetectionTerminalState')
    terminal_state = terminal_state()

    hider_action_selection = ActionSelectionFactory.get_strategy("EpsilonGreedy")
    hider_action_selection = hider_action_selection(epsilon=0.1)

    hider_learning_algorithm = AlgorithmFactory.get_algorithm("QLearning")
    hider_learning_algorithm = hider_learning_algorithm(
        learning_rate=0.1,
        discount_factor=0.99,
        default_q_value=0.0,
    )

    hider_state_processor = StateFactory.get_hider_state('CoordinateState')
    hider_state_processor = hider_state_processor(terminal_state=terminal_state)

    hider_reward_strategy = RewardFactory.get_reward('DurationReward')
    hider_reward_strategy = hider_reward_strategy()

    hider = Agent(
        agent_role=AgentRole.HIDER, 
        learning_algorithm=hider_learning_algorithm,
        action_selection_strategy=hider_action_selection,
        state_processor=hider_state_processor,
        reward_strategy=hider_reward_strategy,
        )
    
    # Create the seeker agent
    seeker_action_selection = ActionSelectionFactory.get_strategy("EpsilonGreedy")
    seeker_action_selection = seeker_action_selection(epsilon=0.1)

    seeker_learning_algorithm = AlgorithmFactory.get_algorithm("QLearning")
    seeker_learning_algorithm = seeker_learning_algorithm(
        learning_rate=0.1,
        discount_factor=0.99,
        default_q_value=0.0,
    )

    seeker_state_processor = StateFactory.get_seeker_state('CoordinateState')
    seeker_state_processor = seeker_state_processor(terminal_state=terminal_state)

    seeker_reward_strategy = RewardFactory.get_reward('DurationReward')
    seeker_reward_strategy = seeker_reward_strategy()

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
    
    # Create the simulation visualizer
    simulation_visualizer = SimulationVisualizerFactory.get_visualizer('GridVisualizer')
    simulation_visualizer = simulation_visualizer()

    # Create the simulation
    simulation = Simulation(
        board=board,
        simulation_visualizer=simulation_visualizer,
        )
    
    simulation.run()


if __name__ == "__main__":
    main()
