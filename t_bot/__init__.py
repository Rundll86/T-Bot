from t_bot.engine.world import GameWorld, WorldRenderer


class TBot:
    def __init__(self) -> None:
        self.world = GameWorld()
        self.world_renderer = WorldRenderer()

    def start(self):
        pass
