from t_bot.engine.world.target import BaseEntity


class SlimeEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("史莱姆", 100, "史")
