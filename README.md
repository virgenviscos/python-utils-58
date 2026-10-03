# python-utils-58

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight Python utility library designed to streamline indie game development workflows, handling common low-level math and state operations. It provides high-performance tools for 2D coordinate systems, directional pathfinding helpers, and precise tick-rate regulators for Pygame or Pyglet loops.

## Features

* **Fast Grid Generator:** Easily construct 2D coordinate grids and adjacency lists for hex and square tile maps.
* **Delta-Time Tick Regulator:** High-accuracy frame-rate controller designed to prevent CPU spikes in continuous rendering loops.
* **Vector2D Math Helpers:** Lightweight mathematical functions for distance calculation, rotation, and linear interpolation without the overhead of heavy scientific libraries.

## Installation

Install the package directly from PyPI:

```bash
pip install python-utils-58
```

## Quick Start

Initialize a map grid and regulate your game loop with just a few lines of code:

```python
from python_utils_58.grid import SquareGrid
from python_utils_58.loop import FrameRegulator

# 1. Generate a 10x10 map grid
game_map = SquareGrid(width=10, height=10)
neighbors = game_map.get_neighbors(x=4, y=5)

# 2. Set up a steady 60 FPS loop
regulator = FrameRegulator(target_fps=60)

running = True
while running:
    # Get delta time in seconds
    dt = regulator.tick()
    
    # Game logic update using dt goes here
    print(f"Loop running. Delta time: {dt:.4f}s")
    
    # Break immediately for demonstration purposes
    running = False
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.