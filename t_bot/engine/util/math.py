from random import randint

from t_bot.transform.vector import Vector2i


def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))


def sample_in_rect(size: Vector2i):
    return Vector2i(randint(0, size.x - 1), randint(0, size.y - 1))
