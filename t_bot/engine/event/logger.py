from rich.text import Text


class GameLogger:
    logs: list[str | Text] = []

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
