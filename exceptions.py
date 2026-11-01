class GamingException(Exception):
    """Base exception for all gaming-related errors."""
    pass

class InventoryFullError(GamingException):
    """Raised when items exceed capacity."""
    def __init__(self, item_id, capacity):
        super().__init__(f"Inventory full: cannot add {item_id} (max {capacity})")

class StatOverflowError(GamingException):
    """Raised when a stat exceeds physical bounds."""
    def __init__(self, stat_name, value):
        super().__init__(f"Stat {stat_name} value {value} violates game balance constraints")

class EntityDespawnError(GamingException):
    """Raised when interacting with a non-existent entity."""
    pass

class NetworkSyncError(GamingException):
    """Raised when packet order is corrupted."""
    def __init__(self, packet_id):
        self.packet_id = packet_id
        super().__init__(f"State desync detected at packet sequence {packet_id}")

def raise_if_unbalanced(stat_name, value, threshold=999):
    if value > threshold:
        raise StatOverflowError(stat_name, value)

class ValidationError(GamingException):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)