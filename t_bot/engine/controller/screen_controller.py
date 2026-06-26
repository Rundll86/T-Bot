import os

from rich.console import Console

from t_bot.engine.event.event_bus import EventBus


class ScreenController(EventBus):
    def __init__(self) -> None:
        super().__init__()
        self.console = Console(highlight=False)

    def clear(self):
        os.system("cls")

    def redraw(self, data: str):
        self.clear()
        self.draw(data)

    def draw(self, data: str):
        self.console.print(data)
