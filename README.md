## Simulation Setup

To run the simulation, follow these steps:

1.  **Download the code from the repository:**
    * Clone the repository using the command:
        ```bash
        git clone https://github.com/jakub-szafranski/marl-hide-and-seek
        ```
    * Navigate to the project directory:
        ```bash
        cd marl-hide-and-seek
        ```
2.  **Install uv:**
    * Execute the command:
        ```bash
        pip install uv
        ```

3.  **Install dependencies using uv:**
    * Execute the command:
        ```bash
        uv sync
        ```

4.  **Configure environment parameters:**
    * In the `config.yml` file, adjust the simulation parameters or leave them as default.

5.  **Run the program:**
    * Execute the command:
        ```bash
        uv run main.py
        ```
