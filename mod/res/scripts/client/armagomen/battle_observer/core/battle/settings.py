from collections import defaultdict

from PlayerEvents import g_playerEvents
from armagomen.battle_observer.core.bo_constants import GLOBAL, MINIMAP, CLOCK, ALIASES, \
    DISPERSION_CIRCLE
from armagomen.utils.common import overrideMethod
from constants import ARENA_GUI_TYPE
from gui.Scaleform.daapi.view.battle.shared.page import SharedPage
from gui.Scaleform.genConsts.BATTLE_VIEW_ALIASES import BATTLE_VIEW_ALIASES
from helpers import dependency
from skeletons.gui.battle_session import IBattleSessionProvider

BATTLES_RANGE = {ARENA_GUI_TYPE.RANDOM,
                 ARENA_GUI_TYPE.UNKNOWN,
                 ARENA_GUI_TYPE.TRAINING,
                 ARENA_GUI_TYPE.RANKED,
                 ARENA_GUI_TYPE.EPIC_RANDOM,
                 ARENA_GUI_TYPE.EPIC_RANDOM_TRAINING,
                 ARENA_GUI_TYPE.SORTIE_2,
                 ARENA_GUI_TYPE.FORT_BATTLE_2,
                 ARENA_GUI_TYPE.TUTORIAL}


class ViewSettings(object):
    @property
    def sessionProvider(self):
        if self.__sessionProvider is None:
            self.__sessionProvider = dependency.instance(IBattleSessionProvider)
        return self.__sessionProvider

    @property
    def isRandomBattle(self):
        return self.sessionProvider.arenaVisitor.gui.isRandomBattle()

    @property
    def isAllowedBattle(self):
        if self.__isAllowed is None:
            self.__isAllowed = False
            arenaVisitor = self.sessionProvider.arenaVisitor
            if arenaVisitor is not None:
                self.__isAllowed = arenaVisitor.getArenaGuiType() in BATTLES_RANGE
        return self.__isAllowed

    def __init__(self, cfg):
        g_playerEvents.onAvatarBecomeNonPlayer += self.clear
        overrideMethod(SharedPage)(self.new_SharedPage_init)
        self.cfg = cfg
        self.__sessionProvider = None
        self.__isAllowed = None
        self.__cache = defaultdict(bool)

    @property
    def cache(self):
        if not self.__cache:
            self.__cache.update({
                ALIASES.HP_BARS: self.cfg.hp_bars[GLOBAL.ENABLED],
                ALIASES.DAMAGE_LOG: (self.cfg.log_total[GLOBAL.ENABLED] or
                                     self.cfg.log_damage_extended[GLOBAL.ENABLED] or
                                     self.cfg.log_input_extended[GLOBAL.ENABLED]),
                ALIASES.MAIN_GUN: self.cfg.main_gun[GLOBAL.ENABLED] and self.isRandomBattle,
                ALIASES.DEBUG: self.cfg.debug_panel[GLOBAL.ENABLED],
                ALIASES.TIMER: self.cfg.battle_timer[GLOBAL.ENABLED],
                ALIASES.SIXTH_SENSE: self.cfg.sixth_sense[GLOBAL.ENABLED],
                ALIASES.TEAM_BASES: self.cfg.team_bases_panel[GLOBAL.ENABLED],
                ALIASES.ARMOR_CALC: self.cfg.armor_calculator[GLOBAL.ENABLED],
                ALIASES.FLIGHT_TIME: self.cfg.flight_time[GLOBAL.ENABLED],
                ALIASES.DISPERSION_TIMER: (self.cfg.dispersion_circle[GLOBAL.ENABLED] and
                                           self.cfg.dispersion_circle[DISPERSION_CIRCLE.TIMER_ENABLED]),
                ALIASES.PANELS: self.cfg.players_panels[GLOBAL.ENABLED],
                ALIASES.MINIMAP: self.cfg.minimap[MINIMAP.ZOOM][GLOBAL.ENABLED] and self.cfg.minimap[GLOBAL.ENABLED],
                ALIASES.USER_BACKGROUND: self.cfg.user_background[GLOBAL.ENABLED],
                ALIASES.WG_COMP: True,
                ALIASES.DATE_TIME: self.cfg.clock[GLOBAL.ENABLED] and self.cfg.clock[CLOCK.IN_BATTLE][GLOBAL.ENABLED]
            })
        return self.__cache

    def new_SharedPage_init(self, base, page, *args, **kwargs):
        base(page, *args, **kwargs)
        config = page._SharedPage__componentsConfig._ComponentsConfig__config
        newConfig = tuple((i, self.checkAndReplaceAlias(aliases)) for i, aliases in config)
        page._SharedPage__componentsConfig._ComponentsConfig__config = newConfig

    def getSetting(self, alias):
        return self.cache[alias] and self.isAllowedBattle

    def clear(self):
        self.__cache.clear()
        self.__isAllowed = None
        self.__sessionProvider = None

    def checkAndReplaceAlias(self, aliases):
        new_aliases = list(aliases)
        if self.getSetting(ALIASES.TEAM_BASES) and BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL in new_aliases:
            new_aliases.remove(BATTLE_VIEW_ALIASES.TEAM_BASES_PANEL)
            new_aliases.append(ALIASES.TEAM_BASES)
        elif self.getSetting(ALIASES.TIMER) and BATTLE_VIEW_ALIASES.BATTLE_TIMER in new_aliases:
            new_aliases.append(ALIASES.TIMER)
        elif self.getSetting(ALIASES.DEBUG) and BATTLE_VIEW_ALIASES.DEBUG_PANEL in new_aliases:
            new_aliases.remove(BATTLE_VIEW_ALIASES.DEBUG_PANEL)
            new_aliases.append(ALIASES.DEBUG)
        elif BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR in new_aliases:
            if self.getSetting(ALIASES.HP_BARS):
                new_aliases.append(ALIASES.HP_BARS)
            if self.getSetting(ALIASES.PANELS):
                new_aliases.append(ALIASES.PANELS)
            if self.getSetting(ALIASES.MAIN_GUN):
                new_aliases.append(ALIASES.MAIN_GUN)
        return tuple(new_aliases)