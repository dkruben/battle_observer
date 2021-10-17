from CurrentVehicle import g_currentVehicle
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import MAIN, CREW_XP
from armagomen.utils.common import logInfo, overrideMethod
from armagomen.utils.dialogs import CrewDialog
from async import async, await
from frameworks.wulf import WindowLayer
from gui.Scaleform.daapi.view.lobby.hangar.Hangar import Hangar
from gui.shared.gui_items.Vehicle import Vehicle
from gui.shared.gui_items.processors.vehicle import VehicleTmenXPAccelerator
from gui.shared.utils import decorators
from gui.veh_post_progression.models.progression import PostProgressionCompletion
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader


class AccelerateCrewXp(object):
    appLoader = dependency.descriptor(IAppLoader)

    def __init__(self):
        self.inProcess = False
        self.dialog = CrewDialog()
        overrideMethod(Hangar, "__onCurrentVehicleChanged")(self.onVehicleChanged)
        overrideMethod(Hangar, "__updateAll")(self.onVehicleChanged)

    @async
    def showDialog(self, vehicle, value, description):
        app = self.appLoader.getApp()
        if app is not None or app.containerManager is not None:
            view = app.containerManager.getView(WindowLayer.VIEW)
            self.dialog.setView(view)
        dialogResult = yield await(self.dialog.showCrewDialog(value, description, vehicle.userName))
        if dialogResult:
            self.accelerateCrewXp(vehicle, value)
        self.inProcess = False

    @decorators.process('updateTankmen')
    def accelerateCrewXp(self, vehicle, value):
        """
        :type value: bool
        :type vehicle: Vehicle
        """
        result = yield VehicleTmenXPAccelerator(vehicle, value, confirmationEnabled=False).request()
        if result.success:
            logInfo("The accelerated crew training is %s for '%s'" % (value, vehicle.userName))

    @staticmethod
    def checkXP(vehicle):
        """
        :type vehicle: Vehicle
        """
        iterator = vehicle.postProgression.iterOrderedSteps()
        return vehicle.xp >= sum(x.getPrice().xp for x in iterator if not x.isRestricted() and not x.isReceived())

    def onVehicleChanged(self, base, *args, **kwargs):
        base(*args, **kwargs)
        if not settings.main[MAIN.CREW_TRAINING] or not g_currentVehicle.isPresent() or self.inProcess:
            return
        vehicle = g_currentVehicle.item  # type: Vehicle
        if not vehicle.isElite or g_currentVehicle.isLocked() or g_currentVehicle.isInBattle():
            return
        value = False
        description = CREW_XP.NED_TURN_OFF
        if vehicle.isFullyElite:
            availability = vehicle.postProgressionAvailability().result
            complete = vehicle.postProgression.getCompletion() is PostProgressionCompletion.FULL
            fullXP = self.checkXP(vehicle)
            if not availability:
                description = CREW_XP.NOT_AVAILABLE
            elif complete:
                description = CREW_XP.IS_FULL_COMPLETE
            elif fullXP:
                description = CREW_XP.IS_FULL_XP
            value = not availability or complete or fullXP
        if vehicle.isXPToTman != value:
            self.inProcess = True
            self.showDialog(vehicle, value, description)


crewXP = AccelerateCrewXp()
