from enum import Enum

from t_bot.transform.vector import Vector2i


class Direction(Vector2i, Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


direction_to_vector = {
    Direction.UP: Vector2i.up(),
    Direction.DOWN: Vector2i.down(),
    Direction.LEFT: Vector2i.left(),
    Direction.RIGHT: Vector2i.right(),
}
vector_to_direction = {
    Vector2i.up(): Direction.UP,
    Vector2i.down(): Direction.DOWN,
    Vector2i.left(): Direction.LEFT,
    Vector2i.right(): Direction.RIGHT,
}
input_to_direction = {
    "w": Direction.UP,
    "s": Direction.DOWN,
    "a": Direction.LEFT,
    "d": Direction.RIGHT,
}
