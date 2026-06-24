from t_bot.engine.world.target import BaseEntity


class PlayerEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("我", 100, "我")
