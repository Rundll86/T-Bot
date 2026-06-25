import msvcrt

from t_bot.engine.event.event_bus import EventBus


class GameController(EventBus):
    def wait_input(self) -> str:
        char = msvcrt.getch().decode("ascii")
        return char
