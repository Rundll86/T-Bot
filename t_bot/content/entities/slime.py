from t_bot.engine.world.target import BaseEntity


class SlimeEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("史莱姆", 100, "史")
        self.speed = 0.5

    def register_events(self):
        super().register_events()

        @self.subscribe(self.my_turn)
        def my_turn():
            self.follow_player()
