from t_bot.engine.renderer import BaseRenderer
from t_bot.engine.renderer.components.player_ui import PlayerUIRenderer
from t_bot.engine.world import GameWorld, WorldRenderer


class GameRenderer(BaseRenderer):
    def __init__(self, world: GameWorld) -> None:
        super().__init__()
        self.world_renderer = WorldRenderer(world)
        self.player_ui_renderer = PlayerUIRenderer(40)

    def render(self) -> None:
        self.add_line(self.world_renderer.redraw())
        self.add_line(self.player_ui_renderer.redraw())
