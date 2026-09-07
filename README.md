# python-utils-58

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight Python utility library designed specifically for Pygame and Pyglet developers to streamline game state management and 2D physics calculations. It simplifies assets loading, vector mathematics, and frame-rate independent state transitions with minimal overhead.

## Features

* **Asset Pipeline:** Automated caching and optimized loading for sprites, audio sheets, and custom TTF fonts.
* **Fast Vector Math:** Helper functions for 2D collision detection (AABB and Circle-Circle) optimized with NumPy integration.
* **Frame-Rate Independent LERP:** Smooth interpolation functions for camera tracking and physics calculations regardless of engine FPS.
* **Modular State Machine:** A clean, event-driven game state manager to handle transitions between menus, loading screens, and active gameplay.

## Installation

Install the package directly from PyPI:

```bash
pip install python-utils-58
```

## Quick Start

The following example demonstrates how to use the vector math and state interpolation modules in your game loop:

```python
import time
from python_utils_58.math import Vector2D, interpolate
from python_utils_58.state import GameStateManager

# Initialize state manager
state_manager = GameStateManager(initial_state="MAIN_MENU")

# Handle smooth camera movement
current_cam = Vector2D(100.0, 150.0)
target_cam = Vector2D(400.0, 300.0)

# Game loop tick (e.g., delta time of 16ms)
dt = 0.016
smooth_factor = 5.0

# Calculate new position
next_frame_cam = interpolate(current_cam, target_cam, smooth_factor * dt)
print(f"New Camera Position: {next_frame_cam.x:.2f}, {next_frame_cam.y:.2f}")

# Switch states safely
state_manager.transition_to("PLAYING")
print(f"Current State: {state_manager.current_state}")
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.