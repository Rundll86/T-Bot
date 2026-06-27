from pathlib import Path

from pygame import mixer

mixer.init()


class AudioController:
    @classmethod
    def play(cls, fp: str):
        sound = mixer.Sound(Path("assets/sounds") / fp)
        return sound.play()
