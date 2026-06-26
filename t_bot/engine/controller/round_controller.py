from t_bot.engine.event.event_subscriber import EventSubscriber


class RoundController:
    time_went: EventSubscriber = EventSubscriber()
    last_input: str = ""
