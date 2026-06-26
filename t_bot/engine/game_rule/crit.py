import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from t_bot.engine.world.target import BaseBullet, BaseEntity


def judge_crit(bullet: "BaseBullet", entity: "BaseEntity"):
    rate = (
        bullet.crit_rate
        + (bullet.launcher.crit_rate if bullet.launcher is not None else 0)
        - entity.anti_crit
    )
    is_crit = random.random() < rate
    dmg = (
        scale_damage(
            bullet.base_damage,
            bullet.launcher.crit_damage if bullet.launcher else 0,
        )
        if is_crit
        else bullet.base_damage
    )
    return is_crit, dmg


def scale_damage(base: float, crit_damage: float):
    return base * (1 + crit_damage)
