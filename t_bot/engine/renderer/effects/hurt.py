from typing import TYPE_CHECKING

from rich.color import Color
from rich.style import Style

from t_bot.engine.controller.round_controller import RoundController
from t_bot.engine.event.logger import GameLogger
from t_bot.engine.renderer.effect import BaseEffect

if TYPE_CHECKING:
    from t_bot.engine.world.target import BaseWorldTarget


class HurtEffect(BaseEffect):
    def run(self, target: "BaseWorldTarget"):
        blend = Style(bgcolor=Color.from_rgb(255, 0, 0))
        target.blends.append(blend)

        @self.subscribe(RoundController.time_went)
        def next_round(input: str):
            GameLogger.add_log("redraw")
            while blend in target.blends:
                GameLogger.add_log("test")
                target.blends.remove(blend)
