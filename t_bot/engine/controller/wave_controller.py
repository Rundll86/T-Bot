from collections.abc import Callable
from random import randint

from pydantic import BaseModel

from t_bot.content.entities.slime import SlimeEntity
from t_bot.engine.controller.game_controller import GameController
from t_bot.engine.util.math import sample_in_rect
from t_bot.engine.world.target import BaseEntity
from t_bot.transform.vector import Vector2i


class EntityPair(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    entity: Callable[[], BaseEntity]
    from_wave: int
    to_wave: int
    per_wave: int
    count: Vector2i


class WaveController:
    current_wave: int = 0
    config: list[EntityPair] = [
        EntityPair(
            entity=SlimeEntity,
            from_wave=0,
            to_wave=-1,
            per_wave=1,
            count=Vector2i(2, 6),
        )
    ]

    @classmethod
    def spawn_current(cls) -> list[BaseEntity]:
        result: list[BaseEntity] = []
        for pair in cls.config:
            if pair.from_wave > cls.current_wave:
                continue
            if pair.to_wave != -1 and cls.current_wave > pair.to_wave:
                continue
            if (cls.current_wave - pair.from_wave) % pair.per_wave != 0:
                continue
            spawn_count = randint(pair.count.x, pair.count.y)
            for _ in range(spawn_count):
                result.append(
                    pair.entity().set_position(
                        sample_in_rect(GameController.world.size)
                    )
                )
        return result

    @classmethod
    def judge_next(cls):
        if GameController.world.enemy_count > 0:
            return
        entities = cls.spawn_current()
        GameController.world.add_target(*entities)
