from engine import (Simulation, SimulationVisualizer, SimulationDataCollector,)

from utils.board_setup import set_up_board, load_config


def main():
    config = load_config('config.yml')
    board = set_up_board(config)
    
    simulation_visualizer = SimulationVisualizer(
        step_delay=config["step_delay"], 
        terminal_delay=config["terminal_delay"],
    )

    # Create the simulation
    if config["visualize"]:
        simulation = Simulation(
            board=board,
            simulation_visualizer=simulation_visualizer,
            )
    else:
        simulation = Simulation(
            board=board,
            )
    
    simulation.run()


if __name__ == "__main__":
    main()
