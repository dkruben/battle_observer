from .base_mod_meta import BaseModMeta


class DispersionTimerMeta(BaseModMeta):

    def __init__(self):
        super(DispersionTimerMeta, self).__init__()

    def as_updateTimerTextS(self, text):
        return self.flashObject.as_upateTimerText(text) if self._isDAAPIInited() else None
