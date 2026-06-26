from t_bot.engine.world.target import BaseEntity


class FlowerEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("花朵", 1, "花")
