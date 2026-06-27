from rich.text import Text

from t_bot.engine.renderer import BaseRenderer
from t_bot.engine.renderer.components.progress_bar import ProgressBarRenderer
from t_bot.engine.util.character import get_space_count
from t_bot.engine.world import GameWorld
from t_bot.engine.world.target import BaseEntity
from t_bot.transform.vector import Vector2i


class ActionQueueRenderer(BaseRenderer):
    def __init__(self, world: GameWorld, width: int = 30, height: int = 15) -> None:
        super().__init__()
        self.world = world
        self.width = width
        self.height = height
        self.padding_height = width - 2

    def render(self) -> None:
        self.add_line(f"┌{'─' * self.padding_height}┐")
        self.add_line(f"│{' ' * self.padding_height}│")
        for _ in range(self.height):
            self.add_line(f"│{' ' * self.padding_height}│")
        self.add_line(f"└{'─' * self.padding_height}┘")
        hd = " 行动队列 "
        hd_w = get_space_count(hd)
        hd_x = 1 + (self.padding_height - hd_w) // 2
        self.auto_replace(Vector2i(hd_x, 0), hd)
        actors = sorted(
            (t for t in self.world.targets if isinstance(t, BaseEntity)),
            key=lambda t: t.action_progress,
            reverse=True,
        )
        bar = ProgressBarRenderer(
            1,
            max_value=1,
            front_char="█",
            front_color="#00ffee",
            back_char="░",
            back_color="#00ffee",
            decorated=False,
        )
        for i in range(self.height):
            if i < len(actors):
                actor = actors[i]
                speed_prefix = Text(
                    f"[+{actor.speed:.2f}]",
                    style="cyan",
                )
                name = Text(
                    actor.display_name,
                    style="white bold",
                )
                progress_text = Text(
                    f"{actor.action_progress:.1f}",
                    style="green" if actor.action_progress > 0.5 else "white",
                )
                bar.length = max(
                    2,
                    self.padding_height
                    - get_space_count(str(speed_prefix))
                    - get_space_count(str(name))
                    - get_space_count(str(progress_text))
                    - 4,
                )
                bar.current_value = actor.action_progress
                bar_str = bar.redraw()
                self.auto_replace(
                    Vector2i(2, 2 + i),
                    Text.assemble(
                        speed_prefix,
                        " ",
                        name,
                        " ",
                        Text.from_markup(bar_str),
                        " ",
                        progress_text,
                    ),
                )
