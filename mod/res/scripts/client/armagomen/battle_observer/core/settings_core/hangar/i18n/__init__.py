from armagomen.bo_constants import GLOBAL
from helpers import getClientLanguage

lang = getClientLanguage().lower()


def getLocalization():
    if GLOBAL.RU_LOCALIZATION:
        from armagomen.battle_observer.core.settings_core.hangar.i18n.ru import translate
    elif lang == "de":
        from armagomen.battle_observer.core.settings_core.hangar.i18n.de import translate
    else:
        from armagomen.battle_observer.core.settings_core.hangar.i18n.en import translate
    return translate


localization = getLocalization()
