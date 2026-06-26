from t_bot.engine.renderer.effect import BaseEffect
from t_bot.engine.world.target import BaseWorldTarget


class StyleBlendEffect(BaseEffect):
    def run(self, target: BaseWorldTarget):
        return super().run(target)
