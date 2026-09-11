"""Gaming exception hierarchy with telemetry and rage-quit metrics."""

from typing import Any, Callable, ClassVar, Dict, Optional


class GameEngineError(Exception):
    """Base exception for all game engine and state anomalies.

    Attributes:
        code: Base numeric error code mapped to the internal telemetry system.
    """

    code: ClassVar[int] = 1000

    def __init__(
        self,
        message: str,
        *,
        code_offset: int = 0,
        **context: Any
    ) -> None:
        super().__init__(message)
        self.error_code: int = self.code + code_offset
        self.context: Dict[str, Any] = context

    def telemetry_payload(self) -> Dict[str, Any]:
        """Generates a structured payload suitable for analytics ingestion."""
        return {
            "error_type": self.__class__.__name__,
            "code": self.error_code,
            "message": str(self),
            "snapshot": self.context,
        }


class OutOfSyncError(GameEngineError):
    """Raised when client and server tick rates drift beyond tolerance."""

    code: ClassVar[int] = 2000

    def __init__(self, client_tick: int, server_tick: int, max_drift: int) -> None:
        drift: int = abs(client_tick - server_tick)
        super().__init__(
            f"Tick desync detected: drift of {drift} frames exceeds threshold {max_drift}.",
            code_offset=drift,
            client_tick=client_tick,
            server_tick=server_tick,
            drift=drift,
        )


class RageQuitTriggered(GameEngineError):
    """Raised when player toxicity or tilt triggers an involuntary session termination."""

    code: ClassVar[int] = 9000

    def __init__(self, player_id: str, tilt_level: float, reason: str = "Unspecified tilt") -> None:
        self.tilt_level: float = max(0.0, min(1.0, tilt_level))
        super().__init__(
            f"Player '{player_id}' force-closed session: {reason} (tilt score: {self.tilt_level:.2f})",
            code_offset=int(self.tilt_level * 99),
            player_id=player_id,
            tilt_level=self.tilt_level,
        )


def handle_game_exception(
    exc: GameEngineError,
    fallback_handler: Optional[Callable[[Dict[str, Any]], None]] = None
) -> Dict[str, Any]:
    """Processes a game engine exception and invokes an optional custom fallback logger."""
    payload: Dict[str, Any] = exc.telemetry_payload()
    if fallback_handler is not None:
        fallback_handler(payload)
    return payload
