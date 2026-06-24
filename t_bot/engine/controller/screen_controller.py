import os

from rich.console import Console

from t_bot.engine.event.event_bus import EventBus


class ScreenController(EventBus):
    def __init__(self) -> None:
        super().__init__()
        self.console = Console(highlight=False)

    def redraw(self, data: str):
        os.system("cls")
        self.console.print(data)
