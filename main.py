from src.environment import Board, SimulationDataCollector, SimulationVisualizer, Simulation
from src.agents import AgentRole
from src.utils.create_agent import create_agent_from_config
import yaml

def main():
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)
        print(f'Config loaded: {config["seeker_learning_algorithm"]}, {config["seeker_state"]}, {config["seeker_reward"]}')
    
    # Create agents
    hider = create_agent_from_config(AgentRole.HIDER, "hider", config)
    seeker = create_agent_from_config(AgentRole.SEEKER, "seeker", config)
    
    # Setup board
    board = Board(hider=hider, seeker=seeker)
    
    # Setup data collector
    simulation_data_collector = SimulationDataCollector(
        q_values_file_path_hider=config["hider_saving_file_path"],
        q_values_file_path_seeker=config["seeker_saving_file_path"],
        data_file_path=config["data_file_path"],
    )
    
    # Create and run simulation
    simulation_args = {
        "board": board,
        "simulation_data_collector": simulation_data_collector
    }
    
    if config["visualize"]:
        simulation_args["simulation_visualizer"] = SimulationVisualizer(
            step_delay=config["step_delay"],
            terminal_delay=config["terminal_delay"],
        )
    
    simulation = Simulation(**simulation_args)
    simulation.run()


if __name__ == "__main__":
    # main()
    def run_experiment():
        main()
        with open("config.yml", "r") as file:
            past_data = file.read()
        config = yaml.safe_load(past_data)

        # modify the data and save it 
        config["hider_from_pretrained"] = True
        config["seeker_from_pretrained"] = True
        config["seeker_initial_epsilon"] = 0
        config["hider_initial_epsilon"] = 0
        config["total_episodes"] = 1000
        with open("config.yml", "w") as file:
            yaml.dump(config, file)

        main()

        # change back 
        with open("config.yml", "w") as file:
            file.write(past_data)

    import json
    import pandas as pd
    import yaml

    configurations = [
        {"seeker_learning_algorithm": "QLearning", "seeker_state": "CompleteKnowledgeState", "seeker_reward": "WinLoseReward"},
        {"seeker_learning_algorithm": "QLearning", "seeker_state": "CompleteKnowledgeState", "seeker_reward": "DurationReward"},
        {"seeker_learning_algorithm": "QLearning", "seeker_state": "HearingStateSeeker", "seeker_reward": "WinLoseReward"},
        {"seeker_learning_algorithm": "QLearning", "seeker_state": "HearingStateSeeker", "seeker_reward": "DurationReward"},
        
        {"seeker_learning_algorithm": "Sarsa", "seeker_state": "CompleteKnowledgeState", "seeker_reward": "WinLoseReward"},
        {"seeker_learning_algorithm": "Sarsa", "seeker_state": "CompleteKnowledgeState", "seeker_reward": "DurationReward"},
        {"seeker_learning_algorithm": "Sarsa", "seeker_state": "HearingStateSeeker", "seeker_reward": "WinLoseReward"},
        {"seeker_learning_algorithm": "Sarsa", "seeker_state": "HearingStateSeeker", "seeker_reward": "DurationReward"},
        
        {"seeker_learning_algorithm": "MonteCarlo", "seeker_state": "CompleteKnowledgeState", "seeker_reward": "WinLoseReward"},
        {"seeker_learning_algorithm": "MonteCarlo", "seeker_state": "CompleteKnowledgeState", "seeker_reward": "DurationReward"},
        {"seeker_learning_algorithm": "MonteCarlo", "seeker_state": "HearingStateSeeker", "seeker_reward": "WinLoseReward"},
        {"seeker_learning_algorithm": "MonteCarlo", "seeker_state": "HearingStateSeeker", "seeker_reward": "DurationReward"},
    ]
    all_data = []
    for index, config in enumerate(configurations):
        print(f"######### RUNNING {index+1} ITERATION ###########")
        print(f"Config: {config}")

        # Change variables
        with open("config.yml", "r") as file:
            past_data = file.read()
        config_data = yaml.safe_load(past_data)
        config_data["seeker_learning_algorithm"] = config["seeker_learning_algorithm"]
        config_data["seeker_state"] = config["seeker_state"]
        config_data["seeker_reward"] = config["seeker_reward"]
        with open("config.yml", "w") as file:
            yaml.dump(config_data, file)

        # run experiment
        data_configuration = {"seeker_accuracy": [], "seeker_reward": [], "hider_accuracy": [], "hider_reward": []}
        for _ in range(50):
            run_experiment()

            with open("data/simulation_data.json", "r") as file:
                data = json.load(file)
            # Convert data to DataFrame
            df = pd.DataFrame(
                {
                    "episode_lengths": data["episode_lengths"],
                    "hider_returns": data["hider_returns"],
                    "seeker_returns": data["seeker_returns"],
                    "winner": data["winner"]
                }
            )

            z = df["winner"].value_counts()
            z = z.to_dict()
            if "AgentRole.SEEKER" not in z:
                z["AgentRole.SEEKER"] = 0
            if "AgentRole.HIDER" not in z:
                z["AgentRole.HIDER"] = 0
            if z["AgentRole.SEEKER"] + z["AgentRole.HIDER"] == 0:
                seeker_accuracy = 0
                hider_accuracy = 0
                
            seeker_accuracy = z['AgentRole.SEEKER'] / (z['AgentRole.SEEKER'] + z['AgentRole.HIDER'])
            hider_accuracy = z['AgentRole.HIDER'] / (z['AgentRole.SEEKER'] + z['AgentRole.HIDER'])
            assert round(seeker_accuracy) == round(1-hider_accuracy)

            data_configuration["seeker_accuracy"].append(seeker_accuracy)
            data_configuration["hider_accuracy"].append(hider_accuracy)

            data_configuration["seeker_reward"].append(df["seeker_returns"].mean())
            data_configuration["hider_reward"].append(df["hider_returns"].mean())
        
        all_data.append({config["seeker_learning_algorithm"] + "_" + config["seeker_state"] + "_" + config["seeker_reward"]: data_configuration})
        # put back original set up
        with open("config.yml", "w") as file:
            file.write(past_data)
    
    # save data
    with open("results2.json", "w") as file:
        print("######## SAVING DATA ###########")
        print(all_data)
        print("######### DATA SAVED ###########")
        json.dump(all_data, file, indent=4)