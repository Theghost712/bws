import asyncio
import time
from typing import Dict, Optional


class RateLimiter:
    """Simple async rate limiter: enforces a minimum interval between requests."""

    def __init__(self, min_interval: float = 4.0):
        self.min_interval = min_interval
        self._last_used: Dict[int, float] = {}
        self._lock = asyncio.Lock()

    async def acquire(self, key: Optional[str] = None) -> None:
        loop_key = key or "default"
        async with self._lock:
            now = time.monotonic()
            last = self._last_used.get(loop_key, 0.0)
            wait = self.min_interval - (now - last)
            if wait > 0:
                await asyncio.sleep(wait)
            self._last_used[loop_key] = time.monotonic()

    def is_allowed(self, key: Optional[str] = None) -> bool:
        loop_key = key or "default"
        now = time.monotonic()
        last = self._last_used.get(loop_key, 0.0)
        allowed = (now - last) >= self.min_interval
        if allowed:
            self._last_used[loop_key] = now
        return allowed
