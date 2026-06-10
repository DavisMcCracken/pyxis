"""In-memory cache with per-entry time-to-live."""

import time
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class _Entry[V]:
    value: V
    expires_at: float


class TTLCache[K, V]:
    """Mapping-like cache whose entries expire after a per-entry TTL.

    Args:
        clock: Monotonic time source; injectable for testing.
    """

    def __init__(self, clock: Callable[[], float] = time.monotonic) -> None:
        self._clock = clock
        self._entries: dict[K, _Entry[V]] = {}

    def set(self, key: K, value: V, *, ttl: float) -> None:
        """Store value under key, expiring ttl seconds from now.

        Raises:
            ValueError: If ttl is not positive.
        """
        if ttl <= 0:
            raise ValueError("ttl must be positive")
        self._entries[key] = _Entry(value, self._clock() + ttl)

    def get(self, key: K, default: V | None = None) -> V | None:
        """Return the live value for key, or default if missing or expired."""
        entry = self._entries.get(key)
        if entry is None:
            return default
        if self._clock() > entry.expires_at:
            del self._entries[key]
            return default
        return entry.value

    def __len__(self) -> int:
        now = self._clock()
        self._entries = {k: e for k, e in self._entries.items() if now <= e.expires_at}
        return len(self._entries)
