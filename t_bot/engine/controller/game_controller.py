import msvcrt
from typing import TYPE_CHECKING, Union

from t_bot.engine.event.event_bus import EventBus

if TYPE_CHECKING:
    from t_bot.engine.world import GameWorld
    from t_bot import PlayerEntity
    from t_bot.engine.world.target import BaseEntity


class GameController(EventBus):
    world: "GameWorld"
    player: "PlayerEntity"
    focus_enemy: Union["BaseEntity", None] = None
    got_score: int = 0

    def wait_input(self) -> str:
        char = msvcrt.getch().decode("utf8")
        return char
