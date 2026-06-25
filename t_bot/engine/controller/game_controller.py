import msvcrt
from typing import TYPE_CHECKING

from t_bot.engine.event.event_bus import EventBus

if TYPE_CHECKING:
    from t_bot.engine.world import GameWorld


class GameController(EventBus):
    world: "GameWorld"

    def __init__(self, world: "GameWorld") -> None:
        self.world = world
        GameController.world = world

    def wait_input(self) -> str:
        char = msvcrt.getch().decode("ascii")
        return char
