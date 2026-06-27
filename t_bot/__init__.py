from t_bot.content.entities.player import PlayerEntity
from t_bot.engine.controller.game_controller import GameController
from t_bot.engine.controller.round_controller import RoundController
from t_bot.engine.controller.screen_controller import ScreenController
from t_bot.engine.controller.wave_controller import WaveController
from t_bot.engine.event.event_bus import EventBus
from t_bot.engine.renderer.components.game import GameRenderer
from t_bot.engine.world import GameWorld
from t_bot.transform.vector import Vector2i


class TBot(EventBus):
    def __init__(self) -> None:
        super().__init__()
        self.world = GameWorld()
        self.game_renderer = GameRenderer(self.world)
        self.game_controller = GameController()
        self.screen_controller = ScreenController()

    def start(self):
        self.world.add_target(PlayerEntity().set_position(Vector2i(5, 5)))
        WaveController.judge_next()

    def redraw(self):
        self.screen_controller.redraw(self.game_renderer.redraw())

    def loop(self):
        self.redraw()
        while True:
            input_char = self.game_controller.wait_input()
            RoundController.last_input = input_char
            self.world.input.emit(input_char)
            RoundController.time_went.emit(input_char)
            self.world.detect_collision()
            self.redraw()
