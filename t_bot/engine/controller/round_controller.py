from t_bot.engine.event.event_subscriber import EventSubscriber


class RoundController:
    """回合控制器 —— 管理"下一回合"事件，世界更新（碰撞检测、寿命递增等）均订阅此事件。"""

    next_round: EventSubscriber = EventSubscriber()
