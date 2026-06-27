from rich.console import Console
from rich.live import Live

from t_bot.engine.event.event_bus import EventBus


class ScreenController(EventBus):
    def __init__(self) -> None:
        super().__init__()
        self.console = Console(highlight=False)
        self.live = Live(
            "WSAD移动，J攻击，Z/X切换武器，按下任意键开始游戏",
            screen=True,
            refresh_per_second=60,
            console=self.console,
        )
        self.live.start()

    def redraw(self, data: str):
        self.live.update(data)

    def stop(self):
        self.live.stop()
