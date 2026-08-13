# Python Utils 58

Python Utils 58 is a collection of utility functions and classes designed for gaming developers. Its purpose is to streamline common tasks, such as game state management, input processing, and asset handling, significantly enhancing the efficiency and effectiveness of game development in Python.

## Features

- **State Management**: Easily manage and switch between different game states (e.g., menu, playing, paused) with an intuitive state machine implementation.
- **Input Handling**: Simplified input management that supports keyboard, mouse, and game controller inputs, allowing for smoother gameplay experiences.
- **Resource Loader**: A robust asset management system that makes loading and unloading textures, sounds, and other game assets painless and efficient.
- **Collision Detection**: Pre-built functions to handle basic collision detection, making it easier to implement physics without diving into complex math.

## Installation

To install Python Utils 58, you can clone the repository and run the setup script. Here are the commands to get started:

```bash
git clone https://github.com/yourusername/python-utils-58.git
cd python-utils-58
pip install .
```

## Basic Usage Example

Here’s a quick example of how to use Python Utils 58 to manage game states:

```python
from python_utils import StateManager

# Create a state manager instance
state_manager = StateManager()

# Define a simple game state
def main_game_state():
    print("Welcome to the Game!")

# Add the game state to the manager
state_manager.add_state("main_game", main_game_state)

# Switch to the desired state
state_manager.switch_state("main_game")
```

This example illustrates how you can define and manage different game states using the StateManager class, thereby enhancing the flow and structure of your game.

![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.