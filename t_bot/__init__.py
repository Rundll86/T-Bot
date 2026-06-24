from rich.console import Console

from t_bot.engine.world import GameWorld, WorldRenderer


class TBot:
    def __init__(self) -> None:
        self.world = GameWorld()
        self.world.init()
        self.world_renderer = WorldRenderer(self.world)
        self.console = Console(highlight=False)

    def print(self):
        self.console.print(self.world_renderer.refresh())

    def start(self):
        self.print()
