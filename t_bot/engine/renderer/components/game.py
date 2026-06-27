from t_bot.engine.renderer import BaseRenderer
from t_bot.engine.renderer.components.action_queue import ActionQueueRenderer
from t_bot.engine.renderer.components.player_ui import PlayerUIRenderer
from t_bot.engine.world import GameWorld, WorldRenderer


class GameRenderer(BaseRenderer):
    def __init__(self, world: GameWorld) -> None:
        super().__init__()
        self.world_renderer = WorldRenderer(world)
        self.player_ui_renderer = PlayerUIRenderer(40)
        self.action_queue_renderer = ActionQueueRenderer(world, height=world.size.y - 1)

    def render(self) -> None:
        world_lines = self.world_renderer.redraw().split("\n")
        action_lines = self.action_queue_renderer.redraw().split("\n")

        for i, line in enumerate(world_lines):
            if i < len(action_lines):
                self.add_line(line + "  " + action_lines[i])
            else:
                self.add_line(line)

        self.add_line(self.player_ui_renderer.redraw())
