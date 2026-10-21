# python-utils-58

`python-utils-58` is a lightweight, high-performance toolkit designed to streamline game development tasks in Python. It provides optimized helpers for real-time memory monitoring, asset management, and cross-platform input handling.

## Features

*   **Memory Tracer:** Track heap usage and object lifecycle in real-time to prevent memory leaks during complex game loops.
*   **Asset Loader:** Asynchronous loading pipeline for textures and audio files, supporting automated caching and validation.
*   **Input Mapper:** Simplify complex input handling by mapping raw keyboard/controller events to custom, remappable game actions.
*   **Frame Stats:** Integrated profiler to calculate and log rolling average frame rates and execution time for specific logic blocks.

## Installation

Install the library directly via pip:

```bash
pip install python-utils-58
```

For development mode, clone the repository and install the dependencies:

```bash
git clone https://github.com/Developer/python-utils-58.git
cd python-utils-58
pip install -r requirements.txt
```

## Usage

Easily monitor your game's performance and manage assets using the built-in decorators and utility classes:

```python
from utils_58 import FrameProfiler, AssetLoader

# Track execution time of the main update loop
@FrameProfiler.log_time
def update_game_state():
    # Game logic here
    pass

# Load a batch of game textures asynchronously
loader = AssetLoader()
loader.load_batch(['player.png', 'background.jpg', 'enemy.png'])
```

## License

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.