class GameLogger:
    logs: list[str] = []

    @classmethod
    def add_log(cls, *data: str) -> None:
        cls.logs.extend(data)

    @classmethod
    def latest(cls) -> str:
        if len(cls.logs) > 0:
            return cls.logs[-1]
        else:
            return ""
