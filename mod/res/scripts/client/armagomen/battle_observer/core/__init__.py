from armagomen.battle_observer.core.battle import BattleCore, ViewSettings
from armagomen.battle_observer.core.observer_core import ObserverCore
from armagomen.battle_observer.settings.config_loader import ConfigLoader
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.utils.keys_parser import HotKeysParser

c_Loader = ConfigLoader(settings)
m_core = ObserverCore()
view_settings = ViewSettings(settings)
b_core = BattleCore(settings)
keysParser = HotKeysParser(settings)
