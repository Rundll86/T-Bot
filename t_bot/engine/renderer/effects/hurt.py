from typing import TYPE_CHECKING

from rich.color import Color
from rich.style import Style

from t_bot.engine.controller.round_controller import RoundController
from t_bot.engine.renderer.effect import BaseEffect

if TYPE_CHECKING:
    from t_bot.engine.world.target import BaseWorldTarget


class HurtEffect(BaseEffect):
    def __init__(self) -> None:
        super().__init__(Style(bgcolor=Color.from_rgb(255, 0, 0)))

    def run(self, target: "BaseWorldTarget"):
        @self.subscribe(RoundController.time_went)
        def time_went(input: str):
            self.exit()
