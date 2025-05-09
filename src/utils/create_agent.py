import json
from src.agents import Agent, AgentRole, ActionSelectionFactory, AlgorithmFactory, StateFactory, RewardFactory, Action


def _load_prelearned_q_values(file_path: str) -> dict:
    with open(file_path, "r") as file:
        prelearned_q_values = json.load(file)

    prelearned_q_values = {
        eval(k): {Action(int(action)): v for action, v in actions.items()} for k, actions in prelearned_q_values.items()
    }
    return prelearned_q_values


def _create_action_selection(strategy_name, initial_epsilon, decay_steps=None, min_epsilon=None):
    strategy = ActionSelectionFactory.get_strategy(strategy_name)
    
    if strategy_name == "EpsilonGreedy":
        return strategy(epsilon=initial_epsilon)
    elif strategy_name == "DecayEpsilonGreedy":
        return strategy(
            epsilon=initial_epsilon,
            decay_steps=decay_steps,
            min_epsilon=min_epsilon
        )


def _create_learning_algorithm(algorithm_name, discount_factor, default_q_value, n_steps,
                             learning_rate=None, prelearned_q_values=None):
    algorithm = AlgorithmFactory.get_algorithm(algorithm_name)(
        discount_factor=discount_factor,
        default_q_value=default_q_value,
    )
    
    if algorithm_name != "MonteCarlo" and learning_rate is not None:
        algorithm.learning_rate = learning_rate
        algorithm.n_steps = n_steps
        
    if prelearned_q_values:
        algorithm.load_prelearned_q_values(prelearned_q_values)
        
    return algorithm


def _create_state_processor(role, state_type):
    if role == AgentRole.HIDER:
        processor_factory = StateFactory.get_hider_state
    elif role == AgentRole.SEEKER:
        processor_factory = StateFactory.get_seeker_state
        
    return processor_factory(state_type)()


def create_agent_from_config(role, config_prefix, config):
    """Create an agent based on configuration parameters."""
    prelearned_q_values = None
    if config[f"{config_prefix}_from_pretrained"]:
        prelearned_q_values = _load_prelearned_q_values(config[f"{config_prefix}_pretrained_file_name"])
    
    action_selection = _create_action_selection(
        config[f"{config_prefix}_action_selection_strategy"],
        config[f"{config_prefix}_initial_epsilon"],
        config["total_episodes"],
        config[f"{config_prefix}_min_epsilon"]
    )
    
    learning_algorithm = _create_learning_algorithm(
        config[f"{config_prefix}_learning_algorithm"],
        config[f"{config_prefix}_discount_factor"],
        config[f"{config_prefix}_default_q_value"],
        config[f"{config_prefix}_n_steps"],
        config[f"{config_prefix}_learning_rate"],
        prelearned_q_values
    )
    
    state_processor = _create_state_processor(role, config[f"{config_prefix}_state"])
    
    reward_strategy = RewardFactory.get_reward(config[f"{config_prefix}_reward"])(role)
    
    return Agent(
        agent_role=role,
        learning_algorithm=learning_algorithm,
        action_selection_strategy=action_selection,
        state_processor=state_processor,
        reward_strategy=reward_strategy,
    )