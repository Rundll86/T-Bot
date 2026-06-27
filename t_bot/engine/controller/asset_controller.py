import os
import __main__


def read_path(*fp: str):
    return os.path.join(os.path.dirname(__main__.__file__), "assets", *fp)


def get_texture(fp: str):
    return open(read_path(f"textures/{fp}"), encoding="utf8").read()
