from rich.color import Color
from rich.style import Style
from rich.text import Text


class GameLogger:
    logs: list[str | Text] = []
    log_lifetime: int = 3

    @classmethod
    def add_log(cls, *data: str | Text) -> None:
        cls.logs.extend(data)

    @classmethod
    def latest(cls) -> str | Text:
        if cls.have_log():
            return cls.logs[-1]
        else:
            return ""

    @classmethod
    def have_log(cls) -> bool:
        return len(cls.logs) > 0

    @classmethod
    def read(cls, count: int) -> list[str | Text]:
        result = []
        time = 0
        for log in reversed(cls.logs):
            result.append(log)
            time += 1
            if time == count:
                break
        while len(result) < count:
            result.append(
                Text(
                    "行动日志...",
                    style=Style(color=Color.from_rgb(100, 100, 100)),
                )
            )
        return result
