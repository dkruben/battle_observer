from armagomen.battle_observer.core import keysParser
from armagomen.bo_constants import MINIMAP
from armagomen.battle_observer.meta.battle.minimap_meta import MinimapMeta
from gui.battle_control import avatar_getter


class Minimap(MinimapMeta):

    def _populate(self):
        super(Minimap, self)._populate()
        keysParser.registerComponent(MINIMAP.HOT_KEY, self.settings[MINIMAP.ZOOM][MINIMAP.HOT_KEY])

    def onEnterBattlePage(self):
        super(Minimap, self).onEnterBattlePage()
        keysParser.onKeyPressed += self.keyEvent
        self.as_startUpdateS(self.settings[MINIMAP.ZOOM][MINIMAP.INDENT])

    def onExitBattlePage(self):
        keysParser.onKeyPressed -= self.keyEvent
        super(Minimap, self).onExitBattlePage()

    def keyEvent(self, key, isKeyDown):
        if key == MINIMAP.HOT_KEY:
            self.as_MinimapCenteredS(isKeyDown)
            avatar_getter.setForcedGuiControlMode(isKeyDown, cursorVisible=isKeyDown)
