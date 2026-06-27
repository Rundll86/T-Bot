from t_bot.engine.renderer import BaseRenderer
from t_bot.engine.util.character import get_space_count
from t_bot.engine.world import GameWorld
from t_bot.engine.world.target import BaseEntity


class ActionQueueRenderer(BaseRenderer):
    """行动队列指示器 —— 放置于世界网格右侧，高度恰好 10 行"""

    def __init__(self, world: GameWorld, width: int = 30) -> None:
        super().__init__()
        self.world = world
        self.width = width
        self.rows = 7
        self._inner = width - 2
        self.bar_front = "█"
        self.bar_back = "░"

    def render(self) -> None:
        hd = " 行动队列 "
        hd_w = get_space_count(hd)
        pad = self._inner - hd_w
        hd_left = pad // 2
        hd_right = pad - hd_left
        self.add_line(f"┌{'─' * hd_left}{hd}{'─' * hd_right}┐")
        self.add_line(f"│{' ' * self._inner}│")

        actors = sorted(
            (t for t in self.world.targets if isinstance(t, BaseEntity)),
            key=lambda t: t.action_progress,
            reverse=True,
        )

        for i in range(self.rows):
            if i < len(actors):
                actor = actors[i]
                name = actor.display_name
                pct = f"{actor.action_progress:.2f}"
                prefix_w = get_space_count(name) + 1 + get_space_count(pct)
                bar_length = max(2, self._inner - prefix_w - 3)
                filled = max(
                    0, min(int(actor.action_progress * bar_length), bar_length)
                )
                bar = self.bar_front * filled + self.bar_back * (bar_length - filled)
                body = f"{name} {bar} {pct}"
                body_w = get_space_count(body)
                pad_r = self._inner - body_w - 1
                self.add_line(f"│ {body}{' ' * pad_r}│")
            else:
                self.add_line(f"│{' ' * self._inner}│")

        self.add_line(f"└{'─' * self._inner}┘")
