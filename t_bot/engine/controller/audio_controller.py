import os
import __main__

from pygame import mixer

mixer.init()


class AudioController:
    @classmethod
    def play(cls, fp: str):
        sound = mixer.Sound(
            os.path.join(os.path.dirname(__main__.__file__), "assets/sounds", fp)
        )
        return sound.play()
