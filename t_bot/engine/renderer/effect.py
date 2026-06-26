from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from t_bot.engine.event.event_bus import EventBus

if TYPE_CHECKING:
    from t_bot.engine.world.target import BaseWorldTarget


class BaseEffect(ABC, EventBus):
    @abstractmethod
    def run(self, target: "BaseWorldTarget"):
        pass

    def apply(self, target: "BaseWorldTarget"):
        self.run(target)
