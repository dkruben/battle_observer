from collections import defaultdict

from PlayerEvents import g_playerEvents
from armagomen.battle_observer.meta.battle.distance_to_enemy_meta import DistanceMeta
from armagomen.constants import GLOBAL, DISTANCE, POSTMORTEM
from armagomen.utils.common import logDebug
from armagomen.utils.timers import CyclicTimerEvent
from constants import ARENA_PERIOD, ARENA_PERIOD_NAMES
from gui.battle_control.avatar_getter import getDistanceToTarget, getInputHandler
from gui.battle_control.battle_constants import PLAYER_GUI_PROPS


class Distance(DistanceMeta):

    def __init__(self):
        super(Distance, self).__init__()
        self.macrosDict = defaultdict(lambda: GLOBAL.CONFIG_ERROR, distance=GLOBAL.ZERO, name=GLOBAL.EMPTY_LINE)
        self.timeEvent = None
        self.isPostmortem = False
        self.vehicles = {}

    def _populate(self):
        super(Distance, self)._populate()
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged += self.as_onCrosshairPositionChangedS
        g_playerEvents.onArenaPeriodChange += self.onArenaPeriodChange

    def _dispose(self):
        ctrl = self.sessionProvider.shared.crosshair
        if ctrl is not None:
            ctrl.onCrosshairPositionChanged -= self.as_onCrosshairPositionChangedS
        g_playerEvents.onArenaPeriodChange -= self.onArenaPeriodChange
        super(Distance, self)._dispose()

    def onArenaPeriodChange(self, period, *args):
        if period == ARENA_PERIOD.BATTLE and self.timeEvent is None:
            self.timeEvent = CyclicTimerEvent(0.5, self.updateDistance)
            self.timeEvent.start()
        elif self.timeEvent is not None:
            self.timeEvent.stop()
            self.timeEvent = None
        logDebug("Distance: onArenaPeriodChange: {}", ARENA_PERIOD_NAMES[period])

    def onBattleSessionStart(self):
        super(Distance, self).onBattleSessionStart()
        handler = getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        feedback = self.sessionProvider.shared.feedback
        if feedback is not None:
            feedback.onVehicleMarkerAdded += self.onVehicleMarkerAdded
            feedback.onVehicleMarkerRemoved += self.onVehicleMarkerRemoved

    def onBattleSessionStop(self):
        if self.timeEvent is not None:
            self.timeEvent.stop()
            self.timeEvent = None
        handler = getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged -= self.onCameraChanged
        feedback = self.sessionProvider.shared.feedback
        if feedback is not None:
            feedback.onVehicleMarkerAdded -= self.onVehicleMarkerAdded
            feedback.onVehicleMarkerRemoved -= self.onVehicleMarkerRemoved
        super(Distance, self).onBattleSessionStop()

    def onVehicleMarkerAdded(self, vProxy, vInfo, guiProps):
        if self.isPostmortem:
            return
        if guiProps == PLAYER_GUI_PROPS.enemy and vProxy.isAlive():
            self.vehicles[vInfo.vehicleID] = vProxy

    def onVehicleMarkerRemoved(self, vehicleID):
        if vehicleID in self.vehicles:
            self.vehicles.pop(vehicleID)

    def updateDistance(self):
        distance = None
        vehicleName = None
        for entity in self.vehicles.itervalues():
            dist = getDistanceToTarget(entity)
            if distance is None or dist < distance:
                distance = dist
                vehicleName = entity.typeDescriptor.type.shortUserString
        if distance is None:
            return self.as_setDistanceS(GLOBAL.EMPTY_LINE)
        self.macrosDict[DISTANCE.TANK_NAME] = vehicleName
        self.macrosDict[DISTANCE.DIST] = distance
        self.as_setDistanceS(self.settings[DISTANCE.TEMPLATE] % self.macrosDict)

    def onCameraChanged(self, ctrlMode, *args, **kwargs):
        self.isPostmortem = ctrlMode in POSTMORTEM.MODES
        if self.isPostmortem:
            if self.timeEvent is not None:
                self.timeEvent.stop()
            self.vehicles.clear()
            self.as_setDistanceS(GLOBAL.EMPTY_LINE)
