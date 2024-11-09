from environment import (Board, SimulationDataCollector, SimulationVisualizer, Simulation)
from agents import (AgentRole, Agent, AlgorithmFactory, ActionSelectionFactory, StateFactory, RewardFactory,)
import json
from environment import Action
import yaml


def load_prelearned_q_values(file_path: str) -> dict:
    with open(file_path, "r") as file:
        prelearned_q_values = json.load(file)
    
    prelearned_q_values = {eval(k): {Action(int(action)): v for action, v in actions.items()} for k, actions in prelearned_q_values.items()}
    return prelearned_q_values

def main():
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)

    if config['from_pretrained_hider']:
        prelearned_q_values_hider = load_prelearned_q_values(config['pretrained_file_name_hider'])
    if config['from_pretrained_seeker']:
        prelearned_q_values_seeker = load_prelearned_q_values(config['pretrained_file_name_seeker'])

    # Create the hider agent
    hider_action_selection = ActionSelectionFactory.get_strategy(config['hider_action_selection_strategy'])
    if config['hider_action_selection_strategy'] == "EpsilonGreedy":
        hider_action_selection = hider_action_selection(epsilon=config['seeker_initial_epsilon'])
    else:
        hider_action_selection = hider_action_selection(
            epsilon=config['hider_initial_epsilon'], 
            decay_steps=config["total_episodes"],
            min_epsilon=config['hider_min_epsilon']
        )

    hider_learning_algorithm = AlgorithmFactory.get_algorithm(config['hider_learning_algorithm'])
    hider_learning_algorithm = hider_learning_algorithm(
        learning_rate=config['hider_learning_rate'],
        discount_factor=config['hider_discount_factor'],
        default_q_value=config['hider_default_q_value'], 
    )
    if config['hider_learning_algorithm'] != "MonteCarlo":
        hider_learning_algorithm.n_steps = config['hider_n_step']
    if config['from_pretrained_hider']:
        hider_learning_algorithm.load_prelearned_q_values(prelearned_q_values_hider)

    if config["hider_state"] == "HearingStateHider":
        state_hider = "HearingStateHider"
    elif config["hider_state"] == "DistanceStateHider":
        state_hider = "DistanceStateHider"
    elif config["hider_state"] == "CompleteKnowledgeState":
        state_hider = "CompleteKnowledgeState"
    else:
        raise ValueError("Invalid seeker state")
    hider_state_processor = StateFactory.get_hider_state(state_hider)
    hider_state_processor = hider_state_processor()

    hider_reward_strategy = RewardFactory.get_reward(config['hider_reward'])
    hider_reward_strategy = hider_reward_strategy(AgentRole.HIDER)

    hider = Agent(
        agent_role=AgentRole.HIDER, 
        learning_algorithm=hider_learning_algorithm,
        action_selection_strategy=hider_action_selection,
        state_processor=hider_state_processor,
        reward_strategy=hider_reward_strategy,
    )
    
    # Create the seeker agent
    seeker_action_selection = ActionSelectionFactory.get_strategy(config['seeker_action_selection_strategy'])

    if config['seeker_action_selection_strategy'] == "EpsilonGreedy":
        seeker_action_selection = seeker_action_selection(epsilon=config['seeker_initial_epsilon'])
    else:
        seeker_action_selection = seeker_action_selection(
            epsilon=config['seeker_initial_epsilon'], 
            decay_steps=config["total_episodes"],
            min_epsilon=config['seeker_min_epsilon']
        )

    seeker_learning_algorithm = AlgorithmFactory.get_algorithm(config['seeker_learning_algorithm'])
    seeker_learning_algorithm = seeker_learning_algorithm(
        learning_rate=config['seeker_learning_rate'],
        discount_factor=config['seeker_discount_factor'],
        default_q_value=config['seeker_default_q_value'],
    )
    if config['seeker_learning_algorithm'] != "MonteCarlo":
        seeker_learning_algorithm.n_steps = config['seeker_n_step']

    if config['from_pretrained_seeker']:
        seeker_learning_algorithm.load_prelearned_q_values(prelearned_q_values_seeker)

    if config["seeker_state"] == "HearingStateSeeker":
        state_seeker = "HearingStateSeeker"
    elif config["seeker_state"] == "DistanceStateSeeker":
        state_seeker = "DistanceStateSeeker"
    elif config["seeker_state"] == "CompleteKnowledgeState":
        state_seeker = "CompleteKnowledgeState"
    else:
        raise ValueError("Invalid seeker state")
    seeker_state_processor = StateFactory.get_seeker_state(state_seeker)
    seeker_state_processor = seeker_state_processor()

    seeker_reward_strategy = RewardFactory.get_reward(config['seeker_reward'])
    seeker_reward_strategy = seeker_reward_strategy(AgentRole.SEEKER)

    seeker = Agent(
        agent_role=AgentRole.SEEKER, 
        learning_algorithm=seeker_learning_algorithm,
        action_selection_strategy=seeker_action_selection,
        state_processor=seeker_state_processor,
        reward_strategy=seeker_reward_strategy,
    )
    
    board = Board(
        hider=hider,
        seeker=seeker,
    )
    
    simulation_visualizer = SimulationVisualizer(
        step_delay=config["step_delay"], 
        terminal_delay=config["terminal_delay"],
    )

    simulation_data_collector = SimulationDataCollector(
        q_values_file_path_hider=config["saving_file_path_hider"],
        q_values_file_path_seeker=config["saving_file_path_seeker"],
    )

    # Create the simulation
    if config["visualize"]:
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
    main()
