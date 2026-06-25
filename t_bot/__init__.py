from t_bot.content.entities.player import PlayerEntity
from t_bot.engine.controller.game_controller import GameController
from t_bot.engine.controller.screen_controller import ScreenController
from t_bot.engine.event.event_bus import EventBus
from t_bot.engine.world import GameWorld, WorldRenderer


class TBot(EventBus):
    def __init__(self) -> None:
        self.game_controller = GameController()
        self.screen_controller = ScreenController()
        super().__init__()
        self.world = GameWorld()
        self.world_renderer = WorldRenderer(self.world)

    def start(self):
        self.world.add_target(PlayerEntity())

    def redraw(self):
        self.screen_controller.redraw(self.world_renderer.redraw())

    def loop(self):
        self.redraw()
        while True:
            input_char = self.game_controller.wait_input()
            print(input_char)
            self.world.input.emit(input_char)
            self.redraw()
