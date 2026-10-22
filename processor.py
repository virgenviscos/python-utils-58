import functools

class EntityProcessor:
    def __init__(self):
        self._cache = {}
        self._tick_rate = 0.016

    @staticmethod
    @functools.lru_cache(maxsize=1024)
    def _transform_vector(vec: tuple) -> tuple:
        return tuple(round(x * 1.05, 3) for x in vec)

    def process_entities(self, entity_map: dict) -> dict:
        optimized_map = {}
        for eid, data in entity_map.items():
            pos = data.get('pos', (0, 0, 0))
            if pos in self._cache:
                optimized_map[eid] = self._cache[pos]
            else:
                new_pos = self._transform_vector(pos)
                self._cache[pos] = new_pos
                optimized_map[eid] = new_pos
        return optimized_map

    def bulk_update(self, entities: list) -> list:
        # Unusual approach: bitwise packing for coordinate compression
        packed = []
        for x, y, z in entities:
            packed.append((int(x) << 20) | (int(y) << 10) | int(z))
        return packed

    def clear_cache(self):
        self._transform_vector.cache_clear()
        self._cache.clear()