from action_selection import ActionSelectionFactory
from environment import (Board, RewardFactory, StateFactory, TerminalState)
from learning import AlgorithmFactory
from agents import AgentRole, Agent
from utils import load_prelearned_q_values

import yaml

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def set_up_board(config):
    terminal_state = TerminalState()
    if config['from_pretrained']:
        prelearned_q_values = load_prelearned_q_values(config['pretrained_file_name'])

    # Create the hider agent
    hider_action_selection = ActionSelectionFactory.get_strategy(config['hider_action_selection_strategy'])
    hider_action_selection = hider_action_selection(
        initial_epsilon=config['hider_initial_epsilon'], 
        decay_rate=config['hider_decay_rate'], 
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
    if config['from_pretrained']:
        hider_learning_algorithm.load_prelearned_q_values(prelearned_q_values['hider_q_values'])

    state_hider = "HearingStateHider"
    hider_state_processor = StateFactory.get_hider_state(state_hider)
    hider_state_processor = hider_state_processor(terminal_state)

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
            initial_epsilon=config['seeker_initial_epsilon'], 
            decay_rate=config['seeker_decay_rate'], 
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

    if config['from_pretrained']:
        seeker_learning_algorithm.load_prelearned_q_values(prelearned_q_values['seeker_q_values'])

    state_seeker = "HearingStateSeeker"
    seeker_state_processor = StateFactory.get_seeker_state(state_seeker)
    seeker_state_processor = seeker_state_processor(terminal_state=terminal_state)

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
    
    return board