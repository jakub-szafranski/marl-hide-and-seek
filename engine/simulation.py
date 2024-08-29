import yaml

# TODO imports, implementations, and method calls are missing


class Simulation:
    def __init__(
        self,
        board,
        hider,
        seeker,
        learning_algorithm,
        reward_strategy,
        terminal_state,
    ) -> None:
        self.board = board
        self.hider = hider
        self.seeker = seeker
        self.learning_algorithm = learning_algorithm
        self.reward_strategy = reward_strategy

        with open("config.yml", "r") as file:
            self.config = yaml.safe_load(file)

    def run(self) -> None:
        total_episodes = self.config["total_episodes"]
        for episode in range(total_episodes):
            self._run_episode()
            self._reset()

    def _run_episode(self) -> None:
        """Run a single episode of the simulation."""
        # while hider and seeker are not in terminal state: ...
        pass

    def _run_step(self, agent) -> None:
        """Run a single step for the given agent."""
        pass

    def _reset(self) -> None:
        self.board.reset()
        self.hider.reset()
        self.seeker.reset()
