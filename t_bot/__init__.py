from random import randint

from t_bot.content.entities.player import PlayerEntity
from t_bot.content.entities.slime import SlimeEntity
from t_bot.engine.controller.game_controller import GameController
from t_bot.engine.controller.round_controller import RoundController
from t_bot.engine.controller.screen_controller import ScreenController
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
        for _ in range(5):
            self.world.add_target(
                SlimeEntity().set_position(Vector2i(randint(1, 8), randint(1, 8)))
            )

    def redraw(self):
        self.screen_controller.clear()
        self.screen_controller.draw(self.game_renderer.redraw())

    def loop(self):
        self.redraw()
        while True:
            input_char = self.game_controller.wait_input()
            self.world.input.emit(input_char)
            RoundController.next_round.emit(input_char)
            self.redraw()
