from __future__ import annotations

import math
from typing import Union, Tuple


class Vector2:
    __slots__ = ("x", "y")

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = float(x)
        self.y = float(y)

    @classmethod
    def from_tuple(cls, t: Tuple[float, float]) -> "Vector2":
        return cls(t[0], t[1])

    @classmethod
    def zero(cls) -> "Vector2":
        return cls(0.0, 0.0)

    @classmethod
    def one(cls) -> "Vector2":
        return cls(1.0, 1.0)

    @classmethod
    def up(cls) -> "Vector2":
        return cls(0.0, -1.0)

    @classmethod
    def down(cls) -> "Vector2":
        return cls(0.0, 1.0)

    @classmethod
    def left(cls) -> "Vector2":
        return cls(-1.0, 0.0)

    @classmethod
    def right(cls) -> "Vector2":
        return cls(1.0, 0.0)

    @property
    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y

    @property
    def length(self) -> float:
        return math.sqrt(self.length_squared)

    @property
    def normalized(self) -> "Vector2":
        length = self.length
        if length == 0.0:
            return Vector2.zero()
        return Vector2(self.x / length, self.y / length)

    @property
    def tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def __neg__(self) -> "Vector2":
        return Vector2(-self.x, -self.y)

    def __abs__(self) -> float:
        return self.length

    def __bool__(self) -> bool:
        return self.x != 0.0 or self.y != 0.0

    def __add__(self, other: Union["Vector2", float, int]) -> "Vector2":
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        if isinstance(other, (int, float)):
            return Vector2(self.x + other, self.y + other)
        return NotImplemented

    def __radd__(self, other: Union[float, int]) -> "Vector2":
        return self.__add__(other)

    def __sub__(self, other: Union["Vector2", float, int]) -> "Vector2":
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        if isinstance(other, (int, float)):
            return Vector2(self.x - other, self.y - other)
        return NotImplemented

    def __rsub__(self, other: Union[float, int]) -> "Vector2":
        if isinstance(other, (int, float)):
            return Vector2(other - self.x, other - self.y)
        return NotImplemented

    def __mul__(self, other: Union["Vector2", float, int]) -> "Vector2":
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        return NotImplemented

    def __rmul__(self, other: Union[float, int]) -> "Vector2":
        return self.__mul__(other)

    def __truediv__(self, other: Union["Vector2", float, int]) -> "Vector2":
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        if isinstance(other, (int, float)):
            return Vector2(self.x / other, self.y / other)
        return NotImplemented

    def __rtruediv__(self, other: Union[float, int]) -> "Vector2":
        if isinstance(other, (int, float)):
            return Vector2(other / self.x, other / self.y)
        return NotImplemented

    def __floordiv__(self, other: Union["Vector2", float, int]) -> "Vector2":
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)
        if isinstance(other, (int, float)):
            return Vector2(self.x // other, self.y // other)
        return NotImplemented

    def __mod__(self, other: Union[float, int]) -> "Vector2":
        if isinstance(other, (int, float)):
            return Vector2(self.x % other, self.y % other)
        return NotImplemented

    def __iadd__(self, other: Union["Vector2", float, int]) -> "Vector2":
        if isinstance(other, Vector2):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, (int, float)):
            self.x += other
            self.y += other
        else:
            return NotImplemented
        return self

    def __isub__(self, other: Union["Vector2", float, int]) -> "Vector2":
        if isinstance(other, Vector2):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, (int, float)):
            self.x -= other
            self.y -= other
        else:
            return NotImplemented
        return self

    def __imul__(self, other: Union["Vector2", float, int]) -> "Vector2":
        if isinstance(other, Vector2):
            self.x *= other.x
            self.y *= other.y
        elif isinstance(other, (int, float)):
            self.x *= other
            self.y *= other
        else:
            return NotImplemented
        return self

    def __itruediv__(self, other: Union["Vector2", float, int]) -> "Vector2":
        if isinstance(other, Vector2):
            self.x /= other.x
            self.y /= other.y
        elif isinstance(other, (int, float)):
            self.x /= other
            self.y /= other
        else:
            return NotImplemented
        return self

    def __ifloordiv__(self, other: Union["Vector2", float, int]) -> "Vector2":
        if isinstance(other, Vector2):
            self.x //= other.x
            self.y //= other.y
        elif isinstance(other, (int, float)):
            self.x //= other
            self.y //= other
        else:
            return NotImplemented
        return self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, Vector2):
            return self.x != other.x or self.y != other.y
        return NotImplemented

    def __len__(self) -> int:
        return 2

    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError(f"Vector2 index out of range: {index}")

    def __iter__(self):
        yield self.x
        yield self.y

    def dot(self, other: "Vector2") -> float:
        return self.x * other.x + self.y * other.y

    def cross(self, other: "Vector2") -> float:
        return self.x * other.y - self.y * other.x

    def distance_to(self, other: "Vector2") -> float:
        return (self - other).length

    def distance_squared_to(self, other: "Vector2") -> float:
        return (self - other).length_squared

    def lerp(self, other: "Vector2", t: float) -> "Vector2":
        return self + (other - self) * t

    def rotated(self, rad: float) -> "Vector2":
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a,
        )

    def angle(self) -> float:
        return math.atan2(self.y, self.x)

    def copy(self) -> "Vector2":
        return Vector2(self.x, self.y)

    def clamp(
        self, x_min: float, x_max: float, y_min: float, y_max: float
    ) -> "Vector2":
        """返回新向量，x 限制在 [x_min, x_max]，y 限制在 [y_min, y_max]。"""
        return Vector2(
            max(x_min, min(self.x, x_max)),
            max(y_min, min(self.y, y_max)),
        )

    def __repr__(self) -> str:
        return f"Vector2({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Vector2i:
    __slots__ = ("x", "y")

    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = int(x)
        self.y = int(y)

    @classmethod
    def from_tuple(cls, t: Tuple[int, int]) -> "Vector2i":
        return cls(t[0], t[1])

    @classmethod
    def zero(cls) -> "Vector2i":
        return cls(0, 0)

    @classmethod
    def one(cls) -> "Vector2i":
        return cls(1, 1)

    @classmethod
    def up(cls) -> "Vector2i":
        return cls(0, -1)

    @classmethod
    def down(cls) -> "Vector2i":
        return cls(0, 1)

    @classmethod
    def left(cls) -> "Vector2i":
        return cls(-1, 0)

    @classmethod
    def right(cls) -> "Vector2i":
        return cls(1, 0)

    def to_vector2(self) -> "Vector2":
        return Vector2(float(self.x), float(self.y))

    def to_vector2i(self) -> "Vector2i":
        return Vector2i(round(self.x), round(self.y))

    def rotated_right(self) -> "Vector2i":
        return Vector2i(self.y, -self.x)

    def rotated_left(self) -> "Vector2i":
        return Vector2i(-self.y, self.x)

    @property
    def length_squared(self) -> int:
        return self.x * self.x + self.y * self.y

    @property
    def length(self) -> float:
        return math.sqrt(float(self.length_squared))

    @property
    def normalized(self) -> "Vector2":
        length = self.length
        if length == 0.0:
            return Vector2.zero()
        return Vector2(self.x / length, self.y / length)

    @property
    def tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def __neg__(self) -> "Vector2i":
        return Vector2i(-self.x, -self.y)

    def __abs__(self) -> float:
        return self.length

    def __bool__(self) -> bool:
        return self.x != 0 or self.y != 0

    def __add__(self, other):
        if isinstance(other, Vector2i):
            return Vector2i(self.x + other.x, self.y + other.y)
        if isinstance(other, int):
            return Vector2i(self.x + other, self.y + other)
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        if isinstance(other, float):
            return Vector2(self.x + other, self.y + other)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Vector2i):
            return Vector2i(self.x - other.x, self.y - other.y)
        if isinstance(other, int):
            return Vector2i(self.x - other, self.y - other)
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        if isinstance(other, float):
            return Vector2(self.x - other, self.y - other)
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(other - self.x, other - self.y)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector2i):
            return Vector2i(self.x * other.x, self.y * other.y)
        if isinstance(other, int):
            return Vector2i(self.x * other, self.y * other)
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        if isinstance(other, float):
            return Vector2(self.x * other, self.y * other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other) -> "Vector2":
        if isinstance(other, (Vector2i, Vector2)):
            return Vector2(self.x / other.x, self.y / other.y)
        if isinstance(other, (int, float)):
            return Vector2(self.x / other, self.y / other)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector2(other / self.x, other / self.y)
        return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, Vector2i):
            return Vector2i(self.x // other.x, self.y // other.y)
        if isinstance(other, int):
            return Vector2i(self.x // other, self.y // other)
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)
        if isinstance(other, float):
            return Vector2(self.x // other, self.y // other)
        return NotImplemented

    def __mod__(self, other):
        if isinstance(other, int):
            return Vector2i(self.x % other, self.y % other)
        return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Vector2i):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, int):
            self.x += other
            self.y += other
        else:
            return NotImplemented
        return self

    def __isub__(self, other):
        if isinstance(other, Vector2i):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, int):
            self.x -= other
            self.y -= other
        else:
            return NotImplemented
        return self

    def __imul__(self, other):
        if isinstance(other, Vector2i):
            self.x *= other.x
            self.y *= other.y
        elif isinstance(other, int):
            self.x *= other
            self.y *= other
        else:
            return NotImplemented
        return self

    def __ifloordiv__(self, other):
        if isinstance(other, Vector2i):
            self.x //= other.x
            self.y //= other.y
        elif isinstance(other, int):
            self.x //= other
            self.y //= other
        else:
            return NotImplemented
        return self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector2i):
            return self.x == other.x and self.y == other.y
        if isinstance(other, Vector2):
            return float(self.x) == other.x and float(self.y) == other.y
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        if isinstance(other, (Vector2i, Vector2)):
            return not self.__eq__(other)
        return NotImplemented

    def __len__(self) -> int:
        return 2

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError(f"Vector2i index out of range: {index}")

    def __iter__(self):
        yield self.x
        yield self.y

    def dot(self, other: Union["Vector2i", "Vector2"]) -> float:
        return self.x * other.x + self.y * other.y

    def cross(self, other: Union["Vector2i", "Vector2"]) -> int:
        return int(self.x * other.y - self.y * other.x)

    def distance_to(self, other: Union["Vector2i", "Vector2"]) -> float:
        return (
            self.to_vector2()
            - (other.to_vector2() if isinstance(other, Vector2i) else other)
        ).length

    def distance_squared_to(self, other: Union["Vector2i", "Vector2"]) -> int:
        dx = self.x - other.x
        dy = self.y - other.y
        return int(dx * dx + dy * dy)

    def manhattan_distance(self, other: "Vector2i") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def angle(self) -> float:
        return math.atan2(float(self.y), float(self.x))

    def copy(self) -> "Vector2i":
        return Vector2i(self.x, self.y)

    def clamp(self, x_min: int, x_max: int, y_min: int, y_max: int) -> "Vector2i":
        """返回新向量，x 限制在 [x_min, x_max]，y 限制在 [y_min, y_max]。"""
        return Vector2i(
            max(x_min, min(self.x, x_max)),
            max(y_min, min(self.y, y_max)),
        )

    def symmetry(self, line: "Vector2i") -> "Vector2i":
        len_sq = line.length_squared
        if len_sq == 0:
            return self.copy()
        dot = self.dot(line)
        factor = 2 * dot / len_sq
        return Vector2i(
            round(factor * line.x - self.x),
            round(factor * line.y - self.y),
        )

    def __repr__(self) -> str:
        return f"Vector2i({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))


Vec2 = Vector2
Vec2i = Vector2i
