class GameLogger:
    logs: list[str] = []

    @classmethod
    def add_log(cls, *data: str) -> None:
        cls.logs.extend(data)

    @classmethod
    def latest(cls) -> str:
        if cls.have_log():
            return cls.logs[-1]
        else:
            return ""

    @classmethod
    def have_log(cls) -> bool:
        return len(cls.logs) > 0
