from t_bot.engine.controller.round_controller import RoundController
from t_bot.engine.world.target import BaseEntity


class SlimeEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("史莱姆", 100, "史")

    def register_events(self):
        super().register_events()

        @self.subscribe(RoundController.next_round)
        def next_round(char: str):
            self.follow_player()
