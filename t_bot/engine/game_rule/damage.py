import random


def damage_float(base: float, range: float = 0.2):
    return base * (1 + random.uniform(-1, 1) * range)
