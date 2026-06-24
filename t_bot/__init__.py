from rich.console import Console

from t_bot.engine.world import GameWorld, WorldRenderer


class TBot:
    def __init__(self) -> None:
        self.world = GameWorld()
        self.world_renderer = WorldRenderer()
        self.console = Console(highlight=False)

    def print(self):
        self.console.print(self.world_renderer.read())

    def start(self):
        self.world_renderer.render()
        self.print()
