from rich.color import Color

from t_bot.engine.world.target import BaseBullet


class SlimeSprintBullet(BaseBullet):
    def __init__(self) -> None:
        super().__init__("危")
        self.foreground = Color.from_rgb(255, 255, 255)
        self.background = Color.from_rgb(255, 0, 0)
        self.hitbox = False
        self.lifetime = 2

    def register_events(self):
        super().register_events()

        @self.subscribe(self.aged)
        def aged(timelifed: int):
            if timelifed > 1:
                self.hitbox = True
