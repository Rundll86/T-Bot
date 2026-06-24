from enum import Enum

from t_bot.transform.vector import Vector2i


class Direction(Vector2i, Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
