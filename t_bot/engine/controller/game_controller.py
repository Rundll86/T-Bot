import msvcrt
import sys

from t_bot.engine.event.event_bus import EventBus
from t_bot.engine.event.event_subscriber import EventSubscriber


class GameController(EventBus):
    def __init__(self) -> None:
        self.input = EventSubscriber()
        super().__init__()

    def wait_input(self) -> str:
        char = msvcrt.getch().decode("ascii")
        self.input.emit(char)
        return char

    def register_events(self):
        super().register_events()

        @self.input.subscribe
        def input(char: str):
            if char == "e":
                sys.exit(0)
