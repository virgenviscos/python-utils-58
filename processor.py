import functools
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class GameState:
    score: int = 0
    entities: list = None

    def __post_init__(self):
        self.entities = self.entities or []

def stage_cleanup(func: Callable):
    @functools.wraps(func)
    def wrapper(state: GameState, *args, **kwargs):
        state.entities = [e for e in state.entities if getattr(e, 'alive', True)]
        return func(state, *args, **kwargs)
    return wrapper

class EntityProcessor:
    def __init__(self, multiplier: float = 1.0):
        self.multiplier = multiplier

    @stage_cleanup
    def process_tick(self, state: GameState, points: int):
        state.score += int(points * self.multiplier)
        for entity in state.entities:
            if hasattr(entity, 'update'):
                entity.update()
        return state.score

class Entity:
    def __init__(self, name: str, alive: bool = True):
        self.name = name
        self.alive = alive

    def update(self):
        pass

def bootstrap_processing(entities: list) -> GameState:
    return GameState(entities=entities)

if __name__ == '__main__':
    proc = EntityProcessor(multiplier=1.5)
    gs = bootstrap_processing([Entity('npc_1'), Entity('npc_2', False)])
    print(f'Initial count: {len(gs.entities)}')
    proc.process_tick(gs, 100)
    print(f'Final count: {len(gs.entities)}')