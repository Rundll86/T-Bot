from __future__ import annotations

from typing import Any, Callable

from t_bot.engine.event.event_subscriber import EventSubscriber


class EventBus:
    def __init__(self) -> None:
        self.subscriptions: list[tuple[EventSubscriber, Callable[..., Any]]] = []
        self.register_events()

    def register_events(self):
        pass

    def subscribe(self, subscriber: EventSubscriber) -> Callable[..., Any]:
        def decorator(callback: Callable[..., Any]):
            subscriber.subscribe(callback)
            self.subscriptions.append((subscriber, callback))
            return callback

        return decorator

    def unsubscribe_all(self) -> None:
        for subscriber, callback in self.subscriptions:
            try:
                subscriber.unsubscribe(callback)
            except Exception:
                pass
        self.subscriptions.clear()

    def __del__(self) -> None:
        self.unsubscribe_all()
