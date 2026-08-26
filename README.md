# python-utils-58

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

python-utils-58 is a Python package that delivers practical utilities for game development and modding. The library includes functions for handling game mechanics efficiently while keeping dependencies minimal.

## Features

- Weighted random selection system for loot, spawns, and AI behaviors
- 2D vector operations with performance optimizations for real-time applications
- Simple entity pooling to reduce object allocation during gameplay
- JSON and pickle based save system with versioning support

## Installation

Clone the repository and install the package:

```bash
git clone https://github.com/Developer/python-utils-58.git
cd python-utils-58
pip install -e .
```

## Usage

```python
from python_utils_58 import weighted_choice, Vector2, EntityPool

# Weighted selection for game drops
loot_table = ['gold', 'potion', 'sword']
weights = [60, 30, 10]
drop = weighted_choice(loot_table, weights)
print(f"Player received: {drop}")

# Basic vector math
velocity = Vector2(5.0, 0.0)
position = Vector2(100, 200) + velocity

# Entity management
pool = EntityPool()
entity = pool.get()
pool.release(entity)
```

## License

This project is licensed under the MIT License.