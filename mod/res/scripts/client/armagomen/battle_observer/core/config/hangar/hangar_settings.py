from gui.vxSettingsApi import vxSettingsApiEvents

from armagomen.battle_observer.core.config.hangar.i18n import localization
from armagomen.battle_observer.core.constants import GLOBAL, CONFIG_INTERFACE, HP_BARS, DISPERSION_CIRCLE, PANELS, \
    SNIPER, MINIMAP, MOD_NAME, MAIN, ANOTHER, URLS
from armagomen.utils.common import logWarning, openWebBrowser
from debug_utils import LOG_CURRENT_EXCEPTION

settingsVersion = 33
KEY_CONTROL = [[29]]
KEY_ALT = [[56]]


class CreateElement(object):

    def __init__(self):
        self.cache = None
        self.getter = None

    def createLabel(self, blockID, varName):
        block = localization.get(blockID, {})
        text = block.get(varName, varName)
        if text == varName:
            return None
        tooltip = block.get('{}_tooltip'.format(varName), GLOBAL.EMPTY_LINE)
        if tooltip:
            tooltip = '{HEADER}%s{/HEADER}{BODY}%s{/BODY}' % (text, tooltip)
        return {'type': 'Label', 'text': text.decode(encoding="utf-8"), 'tooltip': tooltip.decode(encoding="utf-8")}

    @staticmethod
    def createEmpty():
        return {'type': 'Empty'}

    @staticmethod
    def getControlType(value, cType):
        if cType is None:
            if isinstance(value, basestring):
                if value.startswith("#"):
                    return 'TextInputColor'
                return 'TextInputField'
            elif type(value) is bool:
                return 'CheckBox'
        else:
            return cType

    def createControl(self, blockID, varName, value, cType=None):
        result = self.createLabel(blockID, varName)
        if result is not None:
            result.update({'type': self.getControlType(value, cType), 'value': value, 'varName': varName,
                           GLOBAL.WIDTH: 350, 'defaultSelection': False})
            if cType == 'Button':
                result.update({GLOBAL.WIDTH: 250, 'btnName': varName})
        return result

    def createDropDown(self, blockID, varName, options, value):
        result = self.createControl(blockID, varName, value, cType='Dropdown')
        if result is not None:
            result.update({'options': [{'label': x} for x in options]})
        return result

    def createRadioButtonGroup(self, blockID, varName, options, value):
        result = self.createDropDown(blockID, varName, options, value)
        if result is not None:
            result.update(type="RadioButtonGroup")
        return result

    def createHotKey(self, blockID, varName, value, defaultValue):
        result = self.createControl(blockID, varName, value, cType='KeyInput')
        if result is not None:
            result['defaultValue'] = defaultValue
        return result

    def __createNumeric(self, blockID, varName, cType, value, vMin=GLOBAL.ZERO, vMax=GLOBAL.ZERO):
        result = self.createControl(blockID, varName, value, cType=cType)
        if result is not None:
            result.update({'minimum': vMin, 'maximum': vMax})
        return result

    def createStepper(self, blockID, varName, vMin, vMax, step, value):
        result = self.__createNumeric(blockID, varName, 'NumericStepper', value, vMin, vMax)
        if result is not None:
            result.update({'stepSize': step, 'canManualInput': True})
        return result

    def createSlider(self, blockID, varName, vMin, vMax, step, value):
        result = self.__createNumeric(blockID, varName, 'Slider', value, vMin, vMax)
        if result is not None:
            result.update({'snapInterval': step, 'format': '{{value}}'})
        return result

    def createBlock(self, blockID, config, column1, column2):
        name = localization.get(blockID, {}).get("header", blockID)
        result = {
            'modDisplayName': "<font color='#FFFFFF'>{}</font>".format(name),
            'settingsVersion': settingsVersion, GLOBAL.ENABLED: config.get(GLOBAL.ENABLED, True),
            'showToggleButton': GLOBAL.ENABLED in config, 'inBattle': False,
            'position': CONFIG_INTERFACE.BLOCK_IDS.index(blockID), 'column1': column1, 'column2': column2
        }
        return result

    def createItem(self, blockID, key, value):
        val_type = type(value)
        if isinstance(value, basestring):
            if GLOBAL.ALIGN in key:
                return self.createRadioButtonGroup(blockID, key,
                                                   *self.getter.getCollectionIndex(value, GLOBAL.ALIGN_LIST))
            if blockID == HP_BARS.NAME and HP_BARS.STYLE == key:
                return self.createRadioButtonGroup(blockID, key,
                                                   *self.getter.getCollectionIndex(value, HP_BARS.STYLE_SELECT))
        if isinstance(value, (basestring, bool)):
            return self.createControl(blockID, key, value)
        elif val_type is int:
            if DISPERSION_CIRCLE.CIRCLE_SCALE_CONFIG in key:
                return self.createSlider(blockID, key, GLOBAL.ONE, 100, GLOBAL.ONE, value)
            return self.createStepper(blockID, key, -2000, 2000, GLOBAL.ONE, value)
        elif val_type is float:
            if PANELS.ICONS_BLACKOUT in key:
                return self.createStepper(blockID, key, -2.0, 2.0, 0.01, value)
            if GLOBAL.ZERO <= value <= GLOBAL.F_ONE:
                return self.createStepper(blockID, key, GLOBAL.ZERO, 2.0, 0.01, value)
            else:
                return self.createStepper(blockID, key, GLOBAL.ZERO, 300.0, GLOBAL.F_ONE, value)
        elif val_type is list:
            if "_hotkey" in key:
                return self.createHotKey(blockID, key, value, KEY_CONTROL if MINIMAP.HOT_KEY in key else KEY_ALT)
            if SNIPER.STEPS in key:
                return self.createControl(blockID, key, GLOBAL.COMMA_SEP.join((str(x) for x in value)))


class Getter(object):
    __slots__ = ()

    @staticmethod
    def getLinkToParam(config, setting):
        params = setting.split(GLOBAL.C_INTERFACE_SPLITTER)
        for key in params:
            if key in config and isinstance(config[key], dict):
                config = config[key]
        return config, params[GLOBAL.LAST]

    @staticmethod
    def getCollectionIndex(value, collection):
        index = GLOBAL.ZERO
        if value in collection:
            index = collection.index(value)
        return collection, index

    def getKeyPath(self, config, path=()):
        for key, value in config.iteritems():
            key_path = path + (key,)
            if isinstance(value, dict):
                for _path in self.getKeyPath(value, key_path):
                    yield _path
            else:
                yield key_path

    def keyValueGetter(self, config):
        key_val = []
        try:
            for key in sorted(self.getKeyPath(config)):
                key = GLOBAL.C_INTERFACE_SPLITTER.join(key)
                if GLOBAL.ENABLED != key:
                    dic, param = self.getLinkToParam(config, key)
                    key_val.append((key, dic[param]))
        except:
            LOG_CURRENT_EXCEPTION()
        return key_val


class ConfigInterface(CreateElement):

    def __init__(self, modsListApi, vxSettingsApi, config, configLoader):
        super(ConfigInterface, self).__init__()
        self.configLoader = configLoader
        self.modsListApi = modsListApi
        self.config = config
        self.inited = set()
        self.vxSettingsApi = vxSettingsApi
        self.selectedConfig = self.configLoader.configsList.index(self.configLoader.cName)
        self.configSelect = False
        self.getter = Getter()
        vxSettingsApi.addContainer(MOD_NAME, localization['service'], skipDiskCache=True,
                                   useKeyPairs=self.config.main[MAIN.USE_KEY_PAIRS])
        vxSettingsApi.onFeedbackReceived += self.onFeedbackReceived
        vxSettingsApi.onSettingsChanged += self.onSettingsChanged
        vxSettingsApi.onDataChanged += self.onDataChanged

    def addModificationToModList(self):
        """register config window in modsListApi"""
        kwargs = {
            'id': MOD_NAME, 'name': localization['service']['name'],
            'description': localization['service']['description'],
            'icon': 'scripts/client/armagomen/battle_observer/hangar_settings_image.png',
            GLOBAL.ENABLED: True, 'login': True, 'lobby': True, 'callback': self.load_window
        }
        self.modsListApi.addModification(**kwargs)

    def start(self):
        self.addModificationToModList()
        for blockID in CONFIG_INTERFACE.BLOCK_IDS:
            if blockID in self.inited:
                continue
            try:
                self.vxSettingsApi.addMod(MOD_NAME, blockID, lambda *args: self.getTemplate(blockID),
                                          dict(), lambda *args: None, button_handler=self.onButtonPress)
            except Exception as err:
                logWarning('ConfigInterface startLoad {}'.format(repr(err)))
                LOG_CURRENT_EXCEPTION()
            else:
                self.inited.add(blockID)

    def load_window(self):
        """Loading config window"""
        self.vxSettingsApi.loadWindow(MOD_NAME)

    def onUserConfigUpdateComplete(self):
        if self.configSelect:
            for blockID in CONFIG_INTERFACE.BLOCK_IDS:
                self.updateMod(blockID)
            self.load_window()
            self.configSelect = False

    def onFeedbackReceived(self, container, event):
        """Feedback EVENT"""
        if container != MOD_NAME:
            return
        if event == vxSettingsApiEvents.WINDOW_CLOSED:
            if self.configSelect:
                import os
                self.configLoader.createFileInDir(os.path.join(self.configLoader.path, 'load.json'),
                                                  {'loadConfig': self.configLoader.configsList[self.selectedConfig]})
                self.configLoader.readConfig(self.configLoader.configsList[self.selectedConfig])

    def updateMod(self, blockID):
        if blockID not in self.inited:
            try:
                self.vxSettingsApi.updateMod(MOD_NAME, blockID, lambda *args: self.getTemplate(blockID))
            except Exception:
                LOG_CURRENT_EXCEPTION()

    def onSettingsChanged(self, modID, blockID, settings):
        """Saves made by the user settings in the config file."""
        if MOD_NAME != modID:
            return
        if blockID == ANOTHER.CONFIG_SELECT and self.selectedConfig != settings['selectedConfig']:
            self.selectedConfig = settings['selectedConfig']
            self.configSelect = True
            self.inited.clear()
            self.vxSettingsApi.processEvent(MOD_NAME, vxSettingsApiEvents.CALLBACKS.CLOSE_WINDOW)
        else:
            config = getattr(self.config, blockID)
            for setting in settings:
                isString = isinstance(settings[setting], basestring)
                if isString:
                    for pair in GLOBAL.REPLACE:
                        settings[setting] = settings[setting].replace(*pair)
                updatedConfigLink, paramName = self.getter.getLinkToParam(config, setting)
                if paramName in updatedConfigLink:
                    param = settings[setting]
                    if GLOBAL.ALIGN in setting:
                        param = GLOBAL.ALIGN_LIST[param]
                    elif setting == HP_BARS.STYLE and not isString:
                        param = HP_BARS.STYLE_SELECT[param]
                    elif SNIPER.STEPS in setting:
                        param = [round(float(x.strip()), GLOBAL.ONE) for x in param.split(',')]
                    newParamType = type(param)
                    oldParamType = type(updatedConfigLink[paramName])
                    if oldParamType != newParamType:
                        if oldParamType is float and newParamType is int:
                            param = float(param)
                        elif oldParamType is int and newParamType is float:
                            param = int(round(param))
                    updatedConfigLink[paramName] = param
            self.configLoader.updateConfigFile(blockID, config)
            if not self.configSelect:
                self.config.onModSettingsChanged(config, blockID)

    def onDataChanged(self, modID, blockID, varName, value, *a, **k):
        """Darkens dependent elements..."""
        if modID != MOD_NAME or blockID not in CONFIG_INTERFACE.BLOCK_IDS:
            return
        if blockID in CONFIG_INTERFACE.HANDLER_VALUES:
            if varName in CONFIG_INTERFACE.HANDLER_VALUES[blockID]:
                values = CONFIG_INTERFACE.HANDLER_VALUES[blockID][varName]
                if varName in CONFIG_INTERFACE.HANDLER_VALUES["reversed_values"]:
                    if varName == 'dynamic_zoom*enabled':
                        for val in values:
                            self.setHandlerValue(blockID, val, value)
                            value = not value
                        return
                    elif varName == PANELS.BAR_CLASS_COLOR:
                        value = not value
                self.setHandlerValue(blockID, values, value)
        if blockID == MAIN.NAME and varName == MAIN.USE_KEY_PAIRS:
            self.vxSettingsApi.getContainer(MOD_NAME)._vxSettingsCtrl__useHkPairs = value

    def setHandlerValue(self, blockID, data, value):
        getObject = self.vxSettingsApi.getDAAPIObject
        for var in data:
            obj = getObject(blockID, var)
            if obj is not None:
                obj.alpha = 0.4 if not value else GLOBAL.F_ONE
                obj.mouseEnabled = value
                obj.mouseChildren = value
                obj.tabEnabled = value

    @staticmethod
    def onButtonPress(container, blockID, varName, value):
        if container == MOD_NAME and blockID == ANOTHER.CONFIG_SELECT:
            if varName in CONFIG_INTERFACE.DONATE_BUTTONS:
                openWebBrowser(value)

    def getTemplate(self, blockID):
        """create templates, do not change..."""
        config = getattr(self.config, blockID, {})
        column1 = []
        column2 = []
        if blockID == ANOTHER.CONFIG_SELECT:
            column1 = [self.createRadioButtonGroup(blockID, 'selectedConfig',
                                                   self.configLoader.configsList, self.selectedConfig)]
            column2 = [self.createControl(blockID, 'donate_button_ua', URLS.DONATE_UA_URL, 'Button'),
                       self.createControl(blockID, 'donate_button_eu', URLS.DONATE_EU_URL, 'Button'),
                       self.createControl(blockID, 'support_button', URLS.SUPPORT_URL, 'Button')]
        else:
            items = []
            for key, value in self.getter.keyValueGetter(config):
                item = self.createItem(blockID, key, value)
                if item is not None:
                    items.append(item)
            _iter = GLOBAL.ZERO
            middleLen = round(len(items) / 2.0)
            for item in items:
                column = column1 if _iter < middleLen else column2
                column.append(item)
                _iter += GLOBAL.ONE
        return self.createBlock(blockID, config, column1, column2)
