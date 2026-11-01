# python-utils-58

A collection of high-performance Python utilities designed to streamline game development tasks and asset processing. This library provides optimized tools for handling game data, networking, and spatial calculations in Python-based engines.

## Features

*   **Fast Sprite Packer:** Automate texture atlas generation using efficient packing algorithms to minimize memory footprint.
*   **Packet Serializer:** Lightweight binary serialization for real-time multiplayer networking, optimized for low-latency UDP communication.
*   **Spatial Grid Manager:** Rapid 2D/3D collision broad-phase filtering using a dynamic spatial hashing grid.
*   **Save-Data Validator:** Robust schema enforcement for JSON/Binary game save files with automatic version migration support.

## Installation

Install the package via pip:

```bash
pip install python-utils-58
```

To install from source for local development:

```bash
git clone https://github.com/Developer/python-utils-58.git
cd python-utils-58
pip install -e .
```

## Usage

Easily manage entity collision checks using the `SpatialGrid` utility:

```python
from utils_58.spatial import SpatialGrid

# Initialize a grid with 64px cell size
grid = SpatialGrid(cell_size=64)

# Register game entities
grid.insert(entity_id=1, bounds=(10, 10, 32, 32))
grid.insert(entity_id=2, bounds=(50, 50, 32, 32))

# Query nearby entities
neighbors = grid.get_nearby(x=20, y=20, radius=50)
print(f"Entities found in range: {neighbors}")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.