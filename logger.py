import sys
import math
import time
import json
from typing import Any, Dict, Optional

class ResilientGameLogger:
    """A gaming log processor with unusual fault tolerance for corrupted telemetry."""

    LEVEL_MAP = {
        "DEBUG": "\033[94m[HITBOX]\033[0m",
        "INFO": "\033[92m[QUEST]\033[0m",
        "WARN": "\033[93m[DEBUFF]\033[0m",
        "ERROR": "\033[91m[DAMAGE]\033[0m",
        "CRITICAL": "\033[95m[GAME OVER]\033[0m"
    }

    def __init__(self, stream=None, sanitize_nan: bool = True):
        self.stream = stream or sys.stdout
        self.sanitize_nan = sanitize_nan
        self._fallback_stream = sys.stderr

    def _clean_payload(self, data: Any) -> Any:
        """Edge case handler for game telemetry (NaN coordinates, unpicklable entities)."""
        if isinstance(data, float):
            if math.isnan(data) or math.isinf(data):
                return "<OUT_OF_BOUNDS>"
            return round(data, 4)
        if isinstance(data, (bytes, bytearray)):
            return data.decode("utf-8", errors="replace")
        if isinstance(data, dict):
            return {str(k): self._clean_payload(v) for k, v in data.items()}
        if isinstance(data, (list, tuple, set)):
            return [self._clean_payload(x) for x in data]
        if hasattr(data, "__dict__"):
            return self._clean_payload(vars(data))
        return str(data) if not isinstance(data, (int, str, bool, type(None))) else data

    def log(self, level: str, event_name: str, **metadata: Any) -> str:
        """Safely formats and emits log entries even under stream failures or bad input."""
        safe_level = self.LEVEL_MAP.get(str(level).upper(), "[UNKNOWN]")
        safe_event = str(event_name) if event_name is not None else "UNNAMED_EVENT"

        try:
            cleaned = self._clean_payload(metadata) if self.sanitize_nan else metadata
            meta_json = json.dumps(cleaned, default=str)
        except Exception as e:
            meta_json = f'{{"_corrupted": true, "_error": "{type(e).__name__}"}}'

        timestamp = time.strftime("%H:%M:%S")
        entry = f"{timestamp} {safe_level} {safe_event} -> {meta_json}\n"

        try:
            self.stream.write(entry)
            self.stream.flush()
        except (IOError, AttributeError, ValueError):
            try:
                self._fallback_stream.write(f"[FALLBACK LOG] {entry}")
                self._fallback_stream.flush()
            except Exception:
                pass

        return entry.strip()