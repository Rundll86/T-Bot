from t_bot.engine.world.target import BaseCollider, BaseEntity


class PlayerEntity(BaseEntity):
    def __init__(self) -> None:
        super().__init__("我", 100, "我")

    def collide_with(self, other: BaseCollider):
        return super().collide_with(other)
