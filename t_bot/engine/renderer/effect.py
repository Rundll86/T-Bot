from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

from rich.style import Style

from t_bot.engine.event.event_bus import EventBus

if TYPE_CHECKING:
    from t_bot.engine.world.target import BaseWorldTarget


class BaseEffect(ABC, EventBus):
    def __init__(self, style: Style) -> None:
        super().__init__()
        self.style = style
        self.target: Union["BaseWorldTarget", None] = None

    @abstractmethod
    def run(self, target: "BaseWorldTarget"):
        pass

    def apply(self, target: "BaseWorldTarget"):
        self.target = target
        self.run(target)

    def exit(self):
        if self.target is not None:
            while self in self.target.effects:
                self.target.effects.remove(self)
        self.unsubscribe_all()
