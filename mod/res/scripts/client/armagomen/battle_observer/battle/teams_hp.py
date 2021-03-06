from account_helpers.settings_core.settings_constants import GAME, GRAPHICS
from armagomen.battle_observer.core import config, keysParser
from armagomen.battle_observer.core.constants import MARKERS, GLOBAL, HP_BARS, VEHICLE_TYPES, COLORS
from armagomen.battle_observer.meta.battle.team_health_meta import TeamHealthMeta
from gui.battle_control.arena_info.vos_collections import FragCorrelationSortKey
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener
from gui.shared.personality import ServicesLocator

settingsCore = ServicesLocator.settingsCore


class CorrelationMarkers(object):

    def __init__(self, arenaDP):
        self._arenaDP = arenaDP
        self.__allyTeam = self._arenaDP.getNumberOfTeam()
        self.__enemyTeam = self._arenaDP.getNumberOfTeam(enemy=True)
        self.mcColor = config.markers[MARKERS.CLASS_COLOR]
        self.vcColor = config.vehicle_types[VEHICLE_TYPES.CLASS_COLORS]
        self.color = self.updateMarkersColorDict()
        self.enabled = settingsCore.getSetting(GAME.SHOW_VEHICLES_COUNTER)

    def updateMarkersColorDict(self):
        dead_color = config.colors[MARKERS.NAME][MARKERS.DEAD_COLOR]
        blind = MARKERS.ENEMY_COLOR_BLIND if settingsCore.getSetting(GRAPHICS.COLOR_BLIND) else MARKERS.ENEMY
        return {
            self.__allyTeam: {MARKERS.NOT_ALIVE: dead_color, MARKERS.ALIVE: config.colors[MARKERS.NAME][MARKERS.ALLY]},
            self.__enemyTeam: {MARKERS.NOT_ALIVE: dead_color, MARKERS.ALIVE: config.colors[MARKERS.NAME][blind]}
        }

    def getIcon(self, vInfoVO):
        isAlive = vInfoVO.isAlive()
        if self.mcColor and isAlive:
            color = self.vcColor[vInfoVO.vehicleType.classTag]
        else:
            color = self.color[vInfoVO.team][isAlive]
        return MARKERS.ICON.format(color, MARKERS.TYPE_ICON[vInfoVO.vehicleType.classTag])

    def getMarkers(self):
        left, right = [], []
        for vInfoVO in sorted(self._arenaDP.getVehiclesInfoIterator(), key=FragCorrelationSortKey):
            if vInfoVO.team == self.__allyTeam:
                left.append(self.getIcon(vInfoVO))
            else:
                right.append(self.getIcon(vInfoVO))
        return GLOBAL.EMPTY_LINE.join(reversed(left)), GLOBAL.EMPTY_LINE.join(right)


class TeamsHP(TeamHealthMeta, IBattleFieldListener):

    def __init__(self):
        super(TeamsHP, self).__init__()
        self.showAliveCount = config.hp_bars[HP_BARS.ALIVE] and self.isNormalMode
        self.markers = CorrelationMarkers(self._arenaDP) if config.markers[GLOBAL.ENABLED] and self.isNormalMode else None

    def _populate(self):
        super(TeamsHP, self)._populate()
        isColorBlindEnabled = settingsCore.getSetting(GRAPHICS.COLOR_BLIND)
        self.as_startUpdateS(config.hp_bars, isColorBlindEnabled, config.markers)
        if self.markers is not None:
            keysParser.registerComponent(MARKERS.HOT_KEY, config.markers[MARKERS.HOT_KEY])
            keysParser.onKeyPressed += self.keyEvent
            settingsCore.onSettingsApplied += self.onSettingsApplied

    def _dispose(self):
        if self.markers is not None:
            keysParser.onKeyPressed -= self.keyEvent
            settingsCore.onSettingsApplied -= self.onSettingsApplied
        super(TeamsHP, self)._dispose()

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        self.as_updateHealthS(alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP)
        if config.hp_bars[HP_BARS.DIFF]:
            self.as_differenceS(alliesHP - enemiesHP)

    def updateDeadVehicles(self, aliveAllies, deadAllies, aliveEnemies, deadEnemies):
        if self.showAliveCount:
            self.as_updateScoreS(len(aliveAllies), len(aliveEnemies))
        else:
            self.as_updateScoreS(len(deadEnemies), len(deadAllies))
        if self.markers is not None and self.markers.enabled:
            self.as_markersS(*self.markers.getMarkers())

    @property
    def isNormalMode(self):
        random = self._arenaVisitor.gui.isRandomBattle()
        ranked = self._arenaVisitor.gui.isRankedBattle()
        training = self._arenaVisitor.gui.isTrainingBattle()
        return random or ranked or training

    @staticmethod
    def getAlpha():
        return round(min(1.0, config.hp_bars[COLORS.NAME][GLOBAL.ALPHA] * 1.4), 2)

    def keyEvent(self, key, isKeyDown):
        if key == MARKERS.HOT_KEY and isKeyDown:
            settingsCore.applySettings({GAME.SHOW_VEHICLES_COUNTER: not self.markers.enabled})

    def onSettingsApplied(self, diff):
        for name, setting in diff.iteritems():
            if name == GRAPHICS.COLOR_BLIND:
                self.markers.color = self.markers.updateMarkersColorDict()
                if self.markers.enabled:
                    self.as_markersS(*self.markers.getMarkers())
            elif name == GAME.SHOW_VEHICLES_COUNTER:
                self.markers.enabled = bool(setting)
                if self.markers.enabled:
                    self.as_markersS(*self.markers.getMarkers())
                else:
                    self.as_clearMarkersS()
