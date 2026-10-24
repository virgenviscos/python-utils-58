from typing import Dict, Any, List, Optional

class GameStateHandler:
    def __init__(self, initial_state: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the state handler with an optional starting dictionary."""
        self._state: Dict[str, Any] = initial_state or {}

    def update_entity(self, entity_id: str, data: Dict[str, Any]) -> None:
        """Patch entity data into the internal state store."""
        if entity_id not in self._state:
            self._state[entity_id] = {}
        self._state[entity_id].update(data)

    def get_entity_snapshot(self, entity_id: str) -> Dict[str, Any]:
        """Retrieve a deep copy-like snapshot of a specific entity."""
        return {k: v for k, v in self._state.get(entity_id, {}).items()}

    def purge_inactive_entities(self, active_ids: List[str]) -> None:
        """Remove entities not present in the current active frame."""
        self._state = {k: v for k, v in self._state.items() if k in active_ids}

    @property
    def frame_checksum(self) -> int:
        """Generate a unique hash for the current game state."""
        return hash(frozenset((k, tuple(sorted(v.items()))) for k, v in self._state.items()))

def create_handler(init: Optional[Dict[str, Any]] = None) -> GameStateHandler:
    """Factory function for creating state handlers."""
    return GameStateHandler(init)