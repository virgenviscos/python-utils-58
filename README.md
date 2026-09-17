# python-utils-58

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`python-utils-58` is a lightweight Python utility library designed to streamline game development workflows, handling coordinate math, grid navigation, and state serialization. It provides high-performance helpers for 2D grid manipulation and game loop timing, allowing indie developers to focus on gameplay mechanics rather than boilerplate code.

## Features

* **Fast 2D Grid & Pathfinding:** Optimized A* algorithm implementation and coordinate utilities tailored for tile-based 2D games.
* **Game Loop Frame Rate Controller:** A precise delta-time calculator and FPS limiter to ensure consistent game speed across different hardware setups.
* **Robust Save-State Serialization:** Secure binary and JSON compression utilities to handle game state saving and loading seamlessly.

## Installation

Install the package directly from PyPI using pip:

```bash
pip install python-utils-58
```

## Quick Start

Here is a quick example demonstrating how to set up a game grid, find a path, and initialize the frame limiter for your game loop.

```python
from python_utils_58.grid import Grid2D
from python_utils_58.loop import FrameLimiter

# 1. Initialize a 10x10 game grid and block a tile
grid = Grid2D(width=10, height=10)
grid.set_obstacle(x=2, y=2)

# 2. Find a path from start to end coordinates
path = grid.find_path(start=(0, 0), end=(4, 4))
print(f"Path found: {path}")

# 3. Initialize the frame limiter for a 60 FPS target
limiter = FrameLimiter(target_fps=60)

# Example game loop representation
for _ in range(3):
    dt = limiter.tick()
    print(f"Frame rendered in {dt:.4f} seconds")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.