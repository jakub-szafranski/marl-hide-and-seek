## Simulation Setup Instructions

To run the simulation, follow these steps:

1.  **Download the code from the repository:**
    * Clone the repository using the command:
        ```bash
        git clone [https://github.com/jakub-szafranski/marl-hide-and-seek.git](https://github.com/jakub-szafranski/marl-hide-and-seek.git)
        ```
    * Navigate to the project directory:
        ```bash
        cd marl-hide-and-seek
        ```

2.  **Check Python version:**
    * Execute the command:
        ```bash
        python3 --version
        ```
    * Ensure the displayed version is 3.11.6.

3.  **Create a virtual environment:**
    * Execute the command:
        ```bash
        python3 -m venv venv
        ```

4.  **Install uv:**
    * Execute the command:
        ```bash
        pip install uv
        ```

5.  **Install dependencies using uv:**
    * Execute the command:
        ```bash
        uv sync
        ```

6.  **Configure environment parameters:**
    * In the `config.yml` file, adjust the simulation parameters or leave them as default.

7.  **Run the program:**
    * Execute the command:
        ```bash
        uv run main.py
        ```
