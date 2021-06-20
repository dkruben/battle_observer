import os
from shutil import rmtree

from armagomen.battle_observer.components import ComponentsLoader
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.battle_observer.core.update.dialog_button import DialogButtons
from armagomen.battle_observer.core.update.worker import UpdateMain
from armagomen.constants import FILE_NAME, MASSAGES, GLOBAL, CACHE_DIRS, MAIN, \
    MOD_NAME
from armagomen.battle_observer import __version__
from armagomen.utils.common import logInfo, getPreferencesFilePath, getCurrentModPath, logWarning
from gui.Scaleform.daapi.settings import config as packages
from gui.shared.personality import ServicesLocator
from skeletons.gui.app_loader import GuiGlobalSpaceID


class ObserverCore(object):
    __slots__ = ("modsDir", "gameVersion", "workingDir", "fileName", "isFileValid", "mod_version",
                 "configLoader", "moduleLoader", "update", "componentsLoader")

    def __init__(self, configLoader):
        self.configLoader = configLoader
        self.modsDir, self.gameVersion = getCurrentModPath()
        self.workingDir = os.path.join(self.modsDir, self.gameVersion)
        self.fileName = FILE_NAME.format(__version__)
        self.isFileValid = self.isModValidFileName()
        self.mod_version = 'v{0} - {1}'.format(__version__, self.gameVersion)
        self.update = UpdateMain()
        self.update.subscribe()
        self.componentsLoader = ComponentsLoader()

    def clearClientCache(self, category=None):
        path = os.path.normpath(unicode(getPreferencesFilePath(), 'utf-8', errors='ignore'))
        path = os.path.split(path)[GLOBAL.FIRST]
        if category is None:
            for dirName in CACHE_DIRS:
                self.removeDirs(os.path.join(path, dirName), dirName)
        else:
            self.removeDirs(os.path.join(path, category), category)

    @staticmethod
    def removeDirs(normpath, dir_name):
        if os.path.exists(normpath):
            rmtree(normpath, ignore_errors=True, onerror=None)
            logInfo('CLEANING CACHE: {0}'.format(dir_name))

    def onExit(self):
        if self.isFileValid:
            if settings.main[MAIN.AUTO_CLEAR_CACHE]:
                self.clearClientCache()
            logInfo('MOD {0}: {1}'.format(MASSAGES.FINISH, self.mod_version))

    def isModValidFileName(self):
        return self.fileName in os.listdir(self.workingDir)

    def start(self):
        if self.isFileValid:
            logInfo('MOD {0}: {1}'.format(MASSAGES.START, self.mod_version))
            self.componentsLoader.start()
            self.configLoader.start()
            packages.BATTLE_PACKAGES += ("armagomen.battle_observer.battle",)
            packages.LOBBY_PACKAGES += ("armagomen.battle_observer.lobby",)
        else:
            from gui.Scaleform.daapi.view import dialogs
            from gui import DialogsInterface
            locked = MASSAGES.LOCKED_BY_FILE_NAME.format(self.fileName)
            logWarning(locked)

            def loadBlocked(spaceID):
                if spaceID in (GuiGlobalSpaceID.LOGIN, GuiGlobalSpaceID.LOBBY):
                    title = '{0} is locked'.format(MOD_NAME)
                    btn = DialogButtons('Close')
                    DialogsInterface.showDialog(dialogs.SimpleDialogMeta(title, locked, btn), lambda proceed: None)
                    ServicesLocator.appLoader.onGUISpaceEntered -= loadBlocked

            ServicesLocator.appLoader.onGUISpaceEntered += loadBlocked
