# python-utils-58

A collection of lightweight Python utilities designed to streamline game development tasks and asset processing. This toolkit focuses on simplifying data serialization, memory-efficient logging, and performance-critical mathematical operations for indie game projects.

### Features
*   **Asset Packager:** Recursively pack sprite sheets and audio assets into optimized binary blobs to reduce game load times.
*   **Vector Math Suite:** A high-performance set of 2D/3D coordinate manipulation tools optimized for collision detection and trajectory calculation.
*   **Config Hot-Reloader:** Automatically syncs JSON or YAML configuration changes to the game engine state without requiring a full restart.
*   **Event Dispatcher:** A decoupled pub/sub system to manage complex UI and game state interactions with minimal overhead.

### Installation

Requires Python 3.8 or higher. Install directly via pip:

```bash
pip install python-utils-58
```

Alternatively, clone the repository for development:

```bash
git clone https://github.com/developer/python-utils-58.git
cd python-utils-58
pip install -r requirements.txt
```

### Usage

Easily integrate the event dispatcher into your game loop to manage character states or input triggers:

```python
from utils_58 import EventDispatcher

# Initialize the dispatcher
bus = EventDispatcher()

# Define a callback for player interaction
def on_player_jump(data):
    print(f"Player jumped with intensity: {data['force']}")

# Subscribe to the event
bus.subscribe("player_action", on_player_jump)

# Trigger the event elsewhere in your engine
bus.emit("player_action", {"force": 10})
```

### License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Distributed under the MIT License. See `LICENSE` for more information.