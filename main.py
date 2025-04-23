from src.environment import Board, SimulationDataCollector, SimulationVisualizer, Simulation
from src.agents import AgentRole
from src.utils.create_agent import create_agent_from_config
import yaml


def main():
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)
    
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
    main()