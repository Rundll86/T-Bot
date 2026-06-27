from pygame import mixer

from t_bot.engine.controller.asset_controller import read_path

mixer.init()


class AudioController:
    @classmethod
    def play(cls, fp: str):
        sound = mixer.Sound(read_path(f"sounds/{fp}"))
        return sound.play()
