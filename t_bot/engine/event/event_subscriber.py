from __future__ import annotations

import asyncio
import threading
from typing import Any, Callable

C = Callable[..., Any]


class EventSubscriber:
    __slots__ = ("_callbacks", "_lock", "_loop")

    def __init__(self) -> None:
        self._callbacks: list[C] = []
        self._lock = threading.Lock()

    def subscribe(self, callback: C) -> C:
        with self._lock:
            if callback not in self._callbacks:
                self._callbacks.append(callback)
        return callback

    def unsubscribe(self, callback: C) -> None:
        with self._lock:
            try:
                self._callbacks.remove(callback)
            except ValueError:
                pass

    def emit(self, *args: Any, **kwargs: Any) -> None:
        with self._lock:
            cbs = list(self._callbacks)
        for cb in cbs:
            cb(*args, **kwargs)

    async def async_emit(self, *args: Any, **kwargs: Any) -> None:
        with self._lock:
            cbs = list(self._callbacks)

        async def _run(cb: C) -> None:
            try:
                if asyncio.iscoroutinefunction(cb):
                    await cb(*args, **kwargs)
                else:
                    loop = asyncio.get_running_loop()
                    await loop.run_in_executor(None, cb, *args, **kwargs)
            except Exception:
                pass

        await asyncio.gather(*(_run(cb) for cb in cbs), return_exceptions=True)

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.emit(*args, **kwargs)

    def __iadd__(self, callback: C) -> EventSubscriber:
        self.subscribe(callback)
        return self

    def __isub__(self, callback: C) -> EventSubscriber:
        self.unsubscribe(callback)
        return self

    def __len__(self) -> int:
        with self._lock:
            return len(self._callbacks)

    def __bool__(self) -> bool:
        return len(self) > 0

    def __repr__(self) -> str:
        return f"<EventSubscriber subscribers={len(self)}>"
