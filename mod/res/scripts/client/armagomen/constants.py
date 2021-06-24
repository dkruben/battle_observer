from collections import namedtuple

from account_helpers.settings_core.settings_constants import GAME
from aih_constants import SHOT_RESULT, CTRL_MODE_NAME
from gui.Scaleform.daapi.view.battle.shared.crosshair.settings import SHOT_RESULT_TO_DEFAULT_COLOR, \
    SHOT_RESULT_TO_ALT_COLOR
from gui.battle_control.battle_constants import FEEDBACK_EVENT_ID
from gui.shared.gui_items.Vehicle import VEHICLE_CLASS_NAME
from helpers import getClientLanguage

MOD_NAME = "BATTLE_OBSERVER"
FILE_NAME = "armagomen.battleObserver_{}.wotmod"

HEADERS = [('User-Agent', MOD_NAME)]

SWF = namedtuple("SWF", ("BATTLE", "LOBBY", "ATTRIBUTE_NAME"))(
    'modBattleObserver.swf', 'modBattleObserverHangar.swf', 'as_createBattleObserverComp')

URLS = namedtuple("URLS", ("HOST_NAME", "DONATE_UA_URL", "DONATE_EU_URL", "SUPPORT_URL", "UPDATE_GITHUB_API_URL"))(
    "armagomen.bb-t.ru", "https://donatua.com/@armagomen", "https://www.donationalerts.com/r/armagomenvs",
    "https://discord.gg/NuhuhTN", "https://api.github.com/repos/Armagomen/battle_observer/releases/latest")

VEHICLE = namedtuple("VEHICLE", ("CUR", "MAX", "TEAM", "PERCENT"))("health", "maxHealth", "team", "percent")


class GLOBAL:
    def __init__(self):
        pass

    CONFIG_ERROR = "Incorrect macros in config file."
    ONE_SECOND = 1.0
    ALIGN = "align"
    ALIGN_LIST = namedtuple("ALIGN_LIST", ("left", "center", "right"))("left", "center", "right")
    RU_LOCALIZATION = getClientLanguage().lower() in ('ru', 'uk', 'be')
    ALPHA = "alpha"
    BG_ALPHA = "bgAlpha"
    BLUR_X = "blurX"
    BLUR_Y = "blurY"
    COLOR = "color"
    CUSTOM_COLOR = "customColor"
    DOT = "."
    COMMA_SEP = ", "
    EMPTY_LINE = ""
    ENABLED = "enabled"
    FIRST, LAST = (0, -1)
    GLOW_FILTER = "glowFilter"
    HEIGHT = "height"
    IMG = "img"
    INNER = "inner"
    KNOCKOUT = "knockout"
    SCALE = "scale"
    SETTINGS = "settings"
    SMOOTHING = "smoothing"
    STRENGTH = "strength"
    WIDTH = "width"
    X = "x"
    Y = "y"
    ZERO = FIRST
    F_ZERO = float(FIRST)
    ONE = 1
    TWO = 2
    F_ONE = 1.0
    OUTLINE = "outline"
    ICONS_DIR = "img://gui/maps/icons"
    C_INTERFACE_SPLITTER = "*"
    # REPLACE = (
    #     ("\\t", "<tab>"), ("\\n", "<br>"), ("\\r", "<br>")
    # )
    IMG_PARAMS = {"dir": "img://gui/maps/icons/library/efficiency/48x48",
                  "size": "width='24' height='24'",
                  "vspace": "vspace='-13'"}


SERVICE_CHANNEL = namedtuple("SERVICE_CHANNEL", ("NAME", "KEYS", "TYPE", "DATA", "AUX_DATA", "SYSTEM_CHANNEL_KEYS"))(
    "service_channel_filter", "sys_keys", "type", "data", "auxData", (
        "CustomizationForCredits", "CustomizationForGold", "DismantlingForCredits",
        "DismantlingForCrystal", "DismantlingForGold", "Information", "MultipleSelling",
        "PowerLevel", "PurchaseForCredits", "Remove", "Repair", "Restore", "Selling",
        "autoMaintenance", "customizationChanged", "PurchaseForCrystal",
        "PurchaseForGold", "GameGreeting"))


class MAIN:
    def __init__(self):
        pass

    AUTO_CLEAR_CACHE = "autoClearCache"
    ENABLE_BARS_ANIMATION = "enableBarsAnimation"
    ENABLE_FPS_LIMITER = "fps_enableFPSLimiter"
    HIDE_BADGES = "hideBadges"
    HIDE_CHAT = "hideChatInRandom"
    HIDE_CLAN_ABBREV = "hideClanAbbrev"
    HIDE_DOG_TAGS = "hide_dog_tags"
    MAX_FRAME_RATE = "fps_maxFrameRate"
    NAME = "main"
    REMOVE_SHADOW_IN_PREBATTLE = "removeShadowInPrebattle"
    SHOW_FRIENDS = "showFriendsAndClanInEars"
    SHOW_ANONYMOUS = "anonymousEnableShow"
    ANONYMOUS_STRING = "anonymousString"
    CHANGE_ANONYMOUS_NAME = "anonymousNameChange"
    USE_KEY_PAIRS = "useKeyPairs"
    IGNORE_COMMANDERS = "ignore_commanders_voice"
    DISABLE_SCORE_SOUND = "disable_score_sound"
    HIDE_SERVER_IN_HANGAR = "hide_server_in_hangar"
    DEBUG = "DEBUG_MODE"


COLORS = namedtuple("COLORS", (
    "NAME", "BLACK", "BLIND", "B_SILVER", "GOLD", "GREEN", "NORMAL_TEXT", "ORANGE", "RED", "S_YELLOW", "YELLOW",
    "C_GREEN", "C_ORANGE", "C_RED", "C_YELLOW", "C_PURPLE", "C_BG", "GLOBAL", "ALLY_MAME", "ENEMY_MAME",
    "ENEMY_BLIND_MAME", "DEAD_COLOR"))(
    "colors", "#000000", "#6F6CD3", "#858585", "#FFD700", "#5ACB00", "#FAFAFA", "#FF9900", "#F30900", "#E0E06D",
    "#FFC900", "green", "orange", "red", "yellow", "purple", "bgColor", "global", "ally", "enemy", "enemyColorBlind",
    "deadColor")

MAIN_GUN = namedtuple("MAIN_GUN", (
    "NAME", "COLOR", "TEMPLATE", "GUN_ICON", "DONE_ICON", "FAILURE_ICON", "MIN_GUN_DAMAGE", "DAMAGE_RATE"))(
    "main_gun", "mainGunColor", "template", "mainGunIcon", "mainGunDoneIcon", "mainGunFailureIcon", 1000, 0.2)

MINIMAP = namedtuple("MINIMAP", ("NAME", "DEATH_PERMANENT", "HOT_KEY", "INDENT", "SHOW_NAMES", "ZOOM"))(
    "minimap", "permanentMinimapDeath", "zoom_hotkey", "indent", "showDeathNames", "zoom")

HP_BARS = namedtuple("HP_BARS", ("NAME", "STYLE", "WIDTH", "DIFF", "ALIVE", "STYLES"))(
    "hp_bars", "style", "barsWidth", "differenceHP", "showAliveCount",
    namedtuple("HpStyles", ("normal", "league"))("normal", "league"))

CLOCK = namedtuple("CLOCK", (
    "NAME", "IN_BATTLE", "IN_LOBBY", "FORMAT", "UPDATE_INTERVAL", "DEFAULT_FORMAT_BATTLE", "DEFAULT_FORMAT_HANGAR"))(
    "clock", "battle", "hangar", "format", 1.0, "<textformat tabstops='[120]'>%d %b %Y<tab>%X</textformat>",
    "<textformat tabstops='[135]'>%d %b %Y<tab>%X</textformat>")

PREMIUM = namedtuple("PREMIUM", ("PREMIUM_TIME", "PREMIUM_FORMAT", "DEFAULT_FORMAT_PREMIUM"))(
    "premium_time", "premium_format", "<font face='$TitleFont' size='16' color='#FAFAFA'>%(days)d "
                                      "Days. %(hours)02d:%(minutes)02d:%(seconds)02d</font>")


class SNIPER:
    def __init__(self):
        pass

    ZOOM = "zoom"
    NAME = ZOOM
    DYN_ZOOM = "dynamic_zoom"
    STEPS_ONLY = "steps_only"
    ZOOM_STEPS = "zoomSteps"
    STEPS = "steps"
    GUN_ZOOM = "zoomToGunMarker"
    METERS = "zoomXMeters"
    ZOOMS = "zooms"
    ZOOM_EXPOSURE = "zoomExposure"
    INCREASED_ZOOM = "increasedZoom"
    DEFAULT_STEPS = [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 16.0, 20.0, 25.0]
    EXPOSURE_FACTOR, MAX_CALIBER, MAX_DIST = (0.1, 60, 730.0)
    DISABLE_SNIPER = "disable_cam_after_shot"
    DISABLE_LATENCY = "disable_cam_after_shot_latency"
    SKIP_CLIP = "disable_cam_after_shot_skip_clip"
    CLIP = "clip"


class DAMAGE_LOG:
    def __init__(self):
        pass

    NAME = "damage_log"
    ALL_DAMAGES = "allDamages"
    ASSIST_DAMAGE = "assistDamage"
    ASSIST_STUN = "stun"
    ATTACK_REASON = "attackReason"
    AVG_COLOR = "avgColor"
    AVG_DAMAGE = "tankAvgDamage"
    AVG_DAMAGE_DATA = 0.0
    BLOCKED_DAMAGE = "blockedDamage"
    CLASS_COLOR = "tankClassColor"
    MAX_HEALTH = "max_health"
    CLASS_ICON = "classIcon"
    COLOR_MAX_PURPLE, COLOR_MAX_GREEN, COLOR_MULTIPLIER = (0.8333, 0.3333, 255)
    COLOR_FORMAT = "#{:02X}{:02X}{:02X}"
    DAMAGE_AVG_COLOR = "tankDamageAvgColor"
    DAMAGE_LIST = "damageList"
    DONE_EXTENDED = "log_damage_extended"
    D_LOG = "d_log"
    IN_LOG = "in_log"
    TOP_LOG_ASSIST = {FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_KILL_ENEMY, FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_STUN_ENEMY,
                      FEEDBACK_EVENT_ID.PLAYER_USED_ARMOR}
    EXTENDED_DAMAGE = {FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY, FEEDBACK_EVENT_ID.ENEMY_DAMAGED_HP_PLAYER}
    GLOBAL = "log_global"
    HOT_KEY = "logsAltmode_hotkey"
    ICONS = "icons"
    ICON_NAME = "iconName"
    INDEX = "index"
    IN_CENTER = "inCenter"
    KILLED_ICON = "killedIcon"
    KILLS = "kills"
    LAST_DAMAGE = "lastDamage"
    LOG_MAX_LEN = 13
    LOG_MODE = ("extendedLog", "extendedLogALTMODE")
    MAIN_LOG = "main"
    NEW_LINE, COMMA, LIST_SEPARATOR = ("<br>", ", ", " <font color='#FFFF00'>|</font> ")
    PERCENT_AVG_COLOR = "percentDamageAvgColor"
    PLAYER_DAMAGE = "playerDamage"
    RANDOM_MIN_AVG, FRONT_LINE_MIN_AVG = (1200.0, 4000.0)
    RECEIVED_EXTENDED = "log_input_extended"
    REVERSE = "reverse"
    SHELL = ("normal", "gold")
    NORMAL, GOLD = SHELL
    SHELL_COLOR = "shellColor"
    SHELL_TYPE = "shellType"
    SHELL_ICON = "shellIcon"
    SHELL_TYPES = "shellTypes"
    SHELL_ICONS = "shellIcons"
    SHOTS = "shots"
    SPOTTED_TANKS = "spottedTanks"
    STUN_ICON = "stunIcon"
    TANK_LEVEL = "TankLevel"
    TANK_NAME = "tankName"
    TANK_NAMES = "tankNames"
    TEMPLATE_MAIN_DMG = "templateMainDMG"
    TOP_MACROS_NAME = {
        FEEDBACK_EVENT_ID.PLAYER_DAMAGED_HP_ENEMY: PLAYER_DAMAGE,
        FEEDBACK_EVENT_ID.PLAYER_USED_ARMOR: BLOCKED_DAMAGE,
        FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_KILL_ENEMY: ASSIST_DAMAGE,
        FEEDBACK_EVENT_ID.PLAYER_SPOTTED_ENEMY: SPOTTED_TANKS,
        FEEDBACK_EVENT_ID.PLAYER_ASSIST_TO_STUN_ENEMY: ASSIST_STUN,
        FEEDBACK_EVENT_ID.DESTRUCTIBLE_DAMAGED: PLAYER_DAMAGE
    }
    TOP_LOG = "log_total"
    TOTAL_DAMAGE = "totalDamage"
    UNKNOWN_TAG = "unknown"
    USER_NAME = "userName"
    VEHICLE_CLASS = "vehicleClass"
    VEHICLE_CLASS_COLORS = "vehicleClassColors"
    VEHICLE_CLASS_ICON = "vehicleClassIcon"
    WG_ASSIST = "wg_log_hide_assist"
    WG_BLOCKED = "wg_log_hide_block"
    WG_CRITS = "wg_log_hide_crits"
    WG_POS = "wg_log_pos_fix"
    UNDEFINED = "UNDEFINED"
    PREMIUM = "_PREMIUM"
    PREMIUM_SHELLS = {"ARMOR_PIERCING_CR_PREMIUM", "ARMOR_PIERCING_PREMIUM",
                      "HIGH_EXPLOSIVE_PREMIUM", "HOLLOW_CHARGE_PREMIUM"}
    WARNING_MESSAGE = "incorrect event parameter for the damage log"


ARCADE = namedtuple("ARCADE", (
    "NAME", "ANGLE", "DIST_RANGE", "MAX", "MIN", "START_ANGLE", "START_DEAD_DIST", "START_DIST", "SCROLL_MULTIPLE",
    "SCROLL_SENSITIVITY"))(
    "arcade_camera", -0.22, "distRange", "max", "min", "startAngle", "startDeadDist", "startDist", "scrollMultiple",
    "scrollSensitivity")

STRATEGIC = namedtuple("STRATEGIC", ("NAME", "MIN", "MAX", "DIST_RANGE"))("strategic_camera", "min", "max", "distRange")
POSTMORTEM = namedtuple("POSTMORTEM", ("DURATION", "PARAMS", "CAM_MATRIX", "MODES"))(
    "transitionDuration", "postmortemParams", "camMatrix", {CTRL_MODE_NAME.POSTMORTEM, CTRL_MODE_NAME.DEATH_FREE_CAM})


class ARMOR_CALC:
    def __init__(self):
        pass

    GREAT_PIERCED, NOT_PIERCED = 0.75, 1.25
    PIERCING_POWER = "piercingPower"
    NORMAL = SHOT_RESULT_TO_DEFAULT_COLOR[SHOT_RESULT.UNDEFINED]
    NAME = "armor_calculator"
    POSITION = "calcPosition"
    MESSAGES = "messages"
    TEMPLATE = "template"
    MACROS_COLOR = "color"
    MACROS_COUNTED_ARMOR = "countedArmor"
    MACROS_ARMOR = "armor"
    MACROS_PIERCING_RESERVE = "piercingReserve"
    MACROS_MESSAGE = "message"
    MACROS_CALIBER = "caliber"
    RICOCHET = "ricochet"
    NO_DAMAGE = "noDamage"
    MESSAGE_COLORS = set(SHOT_RESULT_TO_ALT_COLOR.itervalues())
    MESSAGE_COLORS.update(SHOT_RESULT_TO_DEFAULT_COLOR.itervalues())
    MESSAGES_TEMPLATE = {key: "<font size='20' color='#FAFAFA'>Change me in config.</font>" for key in MESSAGE_COLORS}
    RICOCHET_MESSAGE = "Ricochet"
    NO_DAMAGE_MESSAGE = "critical shot, no damage"
    DEFAULT_TEMPLATE = "<p align='center'>%(ricochet)s%(noDamage)s<br>" \
                       "<font color='%(color)s'>%(countedArmor)d | %(piercingPower)d</font></p>"


class MARKERS:
    def __init__(self):
        pass

    NAME = "markers"
    HOT_KEY = "showMarkers_hotkey"
    CLASS_COLOR = "markersClassColor"
    TYPE_ICON = {
        VEHICLE_CLASS_NAME.HEAVY_TANK: "H",
        VEHICLE_CLASS_NAME.MEDIUM_TANK: "M",
        VEHICLE_CLASS_NAME.AT_SPG: "J",
        VEHICLE_CLASS_NAME.SPG: "S",
        VEHICLE_CLASS_NAME.LIGHT_TANK: "L",
        "unknown": "U"
    }
    ICON = "<font color='{0}'>{1}</font>"


CAROUSEL = namedtuple("CAROUSEL", ("NAME", "SMALL", "ROWS", "SETTINGS"))(
    "tank_carousel", "smallDoubleCarousel", "carouselRows", {GAME.CAROUSEL_TYPE: None, GAME.DOUBLE_CAROUSEL_TYPE: None})

USER_BACKGROUND = namedtuple("USER_BACKGROUND", ("NAME", "CENTERED_X", "CENTERED_Y", "LAYER"))(
    "user_background", "centeredX", "centeredY", "layer")

FLIGHT_TIME = namedtuple("FLIGHT_TIME", ("NAME", "SPG_ONLY", "TEMPLATE", "M_FLIGHT_TIME", "M_DISTANCE", "ALIGN"))(
    "flight_time", "spgOnly", "template", "flightTime", "distance", "align")

VEHICLE_TYPES = namedtuple("VEHICLE_TYPES", ("NAME", "CLASS_COLORS", "CLASS_ICON", "UNKNOWN", "TEMPLATE"))(
    "vehicle_types", "vehicleClassColors", "vehicleClassIcon", "unknown",
    "<font face='BattleObserver' size='20'>{}</font>")

SIXTH_SENSE = namedtuple("SIXTH_SENSE", (
    "NAME", "SHOW_TIMER", "PLAY_TICK_SOUND", "TIME", "TIMER", "TEMPLATE", "IMAGE", "M_TIME", "M_TIME_LEFT"))(
    "sixth_sense", "showTimer", "playTickSound", "lampShowTime", "timer", "TimerTemplate", "image", "lampTime",
    "timeLeft")


class DISPERSION:
    def __init__(self):
        pass

    NAME = "dispersion_circle"
    CIRCLE_EXTRA_LAP = "circle_extraServerLap"
    CIRCLE_REPLACE = "circle_replaceOriginalCircle"
    CIRCLE_SCALE_CONFIG = "circle_scale"
    CIRCLE_SERVER = "useServerAim"
    ENABLED = "circle_enabled"
    CIRCLE_SCALE = 0.8
    SCALE = 80
    MAX_TIME = 5.0
    SPG_GM_SCALE = 0.8
    GUN_MARKER_MIN_SIZE = 16.0
    MINUS_ONE_F = -1.0

    TIMER_ENABLED = "timer_enabled"
    TIMER_POSITION_X = "timer_position_x"
    TIMER_POSITION_Y = "timer_position_y"
    TIMER_COLOR = "timer_color"
    TIMER_DONE_COLOR = "timer_done_color"
    TIMER_DONE_TEMPLATE = "timer_done_template"
    TIMER_REGULAR_TEMPLATE = "timer_regular_template"
    TIMER_ALIGN = "timer_align"


DEBUG_PANEL = namedtuple("DEBUG_PANEL", (
    "NAME", "TEXT", "TEMPLATE", "GRAPHICS", "PING_BAR", "FPS_BAR", "FPS_COLOR", "PING_COLOR", "LAG_COLOR", "PING",
    "FPS", "LAG"))("debug_panel", "debugText", "text", "debugGraphics", "pingBar", "fpsBar", "fpsColor", "pingColor",
                   "pingLagColor", "PING", "FPS", "PingLagColor")

BATTLE_TIMER = namedtuple("BATTLE_TIMER", (
    "NAME", "TEMPLATE", "COLOR", "END_COLOR", "M_TIMER", "TIME_FORMAT", "START_STRING", "END_BATTLE_SEC"))(
    "battle_timer", "timerTemplate", "timerColor", "timerColorEndBattle", "timer", "%02d:%02d", "00:00", 120)

EFFECTS = namedtuple("EFFECTS", (
    "NAME", "NO_FLASH_BANG", "NO_SHOCK_WAVE", "NO_BINOCULARS", "IS_PLAYER_VEHICLE", "SHOW_FLASH_BANG",
    "SHOW_SHOCK_WAVE"))(
    "effects", "noFlashBang", "noShockWave", "noBinoculars", "isPlayerVehicle", "showFlashBang", "showShockWave")

TEAM_BASES = namedtuple("TEAM_BASES", (
    "NAME", "TEXT_SETTINGS", "FONT", "SIZE", "BOLD", "ITALIC", "UNDERLINE", "BASE_FONT", "FONT_SIZE", "HUNDRED"))(
    "team_bases_panel", "text_settings", "font", "size", "bold", "italic", "underline", "$TitleFont", 16, 100.0)

ALIASES = namedtuple("ALIASES", (
    "HP_BARS", "DAMAGE_LOG", "MAIN_GUN", "DEBUG", "TIMER", "SIXTH_SENSE", "TEAM_BASES", "ARMOR_CALC", "FLIGHT_TIME",
    "DISPERSION_TIMER", "PANELS", "MINIMAP", "USER_BACKGROUND", "WG_COMP", "DATE_TIME"))(
    "Observer_TeamsHP_UI", "Observer_DamageLog_UI", "Observer_MainGun_UI", "Observer_DebugPanel_UI",
    "Observer_BattleTimer_UI", "Observer_SixthSense_UI", "Observer_TeamBases_UI", "Observer_ArmorCalculator_UI",
    "Observer_FlightTime_UI", "Observer_DispersionTimer_UI", "Observer_PlayersPanels_UI", "Observer_Minimap_UI",
    "Observer_UserBackGround_UI", "Observer_WGCompSettings_UI", "Observer_DateTimes_UI")


class PANELS:
    def __init__(self):
        pass

    PANELS_NAME = "players_panels"
    # icons
    ICONS_BLACKOUT = "panels_icon_filter_strength"
    ICONS_ENABLED = "panels_icon_enabled"
    # hp_bars
    BARS_ENABLED = "players_bars_enabled"
    BAR_SETTINGS = "players_bars_settings"
    TEXT_SETTINGS = "players_bars_text"
    BAR = "players_bars_bar"
    HP_TEMPLATE = "players_bars_hp_text"
    ON_KEY_DOWN = "players_bars_on_key_pressed"
    BAR_HOT_KEY = "players_bars_hotkey"
    BAR_CLASS_COLOR = "players_bars_classColor"
    # players_damages
    DAMAGES_ENABLED = "players_damages_enabled"
    DAMAGES_TEMPLATE = "players_damages_text"
    DAMAGES_SETTINGS = "players_damages_settings"
    DAMAGES_HOT_KEY = "players_damages_hotkey"
    DAMAGES_TF = "DamageTf"
    # another
    SPOTTED_FIX = "panels_spotted_fix"
    DAMAGE = "damage"
    TEAM = ("green", "red")


SAVE_SHOOT = namedtuple("SAVE_SHOOT", ("NAME", "MSG", "TEMPLATE", "DESTROYED_BLOCK", "VEHICLE", "TEAM", "HOT_KEY"))(
    "save_shoot", "msg", "Shot blocked.", "block_on_destroyed", "Vehicle", "team", "shoot_hotkey")

ANOTHER = namedtuple("ANOTHER", (
    "CONFIG_SELECT", "SHADOW_SETTINGS", "FRIEND_LIST", "ACCOUNT_DBID", "USERS", "DBID", "BADGES", "IS_TEAM_KILLER",
    "NAME", "CLAN_DBID", "CLAN_ABBR"))(
    "configSelect", "shadow_settings", "friendList", "accountDBID", "users", "databaseID", "badges", "isTeamKiller",
    "name", "clanDBID", "clanAbbrev")

MESSAGES = namedtuple("MESSAGES", ("START", "FINISH", "LOCKED_BY_FILE_NAME", "UPDATE_CHECKED", "NEW_VERSION"))(
    "START LOADING", "SHUTTING DOWN", "ERROR: file {} is not valid, mod locked, please install mod from official site",
    "The update check is completed, you have the current version.",
    "An update {} is detected, the client will be restarted at the end of the download.")

LOAD_LIST = (
    HP_BARS.NAME, MAIN.NAME, MAIN_GUN.NAME, DEBUG_PANEL.NAME, BATTLE_TIMER.NAME, DISPERSION.NAME,
    VEHICLE_TYPES.NAME, SNIPER.NAME, COLORS.NAME, ARMOR_CALC.NAME, TEAM_BASES.NAME, FLIGHT_TIME.NAME,
    SERVICE_CHANNEL.NAME, ARCADE.NAME, STRATEGIC.NAME, PANELS.PANELS_NAME, MINIMAP.NAME, EFFECTS.NAME,
    DAMAGE_LOG.GLOBAL, DAMAGE_LOG.TOP_LOG, DAMAGE_LOG.DONE_EXTENDED, DAMAGE_LOG.RECEIVED_EXTENDED, SAVE_SHOOT.NAME,
    SIXTH_SENSE.NAME, USER_BACKGROUND.NAME, ANOTHER.SHADOW_SETTINGS, CAROUSEL.NAME, CLOCK.NAME
)

CACHE_DIRS = (
    "account_caches", "battle_results", "clan_cache", "custom_data", "dossier_cache", "messenger_cache",
    "storage_cache", "tutorial_cache", "veh_cmp_cache", "web_cache", "profile"
)


class CONFIG_INTERFACE:
    def __init__(self):
        pass

    DONATE_BUTTONS = ('donate_button_ua', 'donate_button_ru', 'donate_button_eu', 'support_button')
    BLOCK_IDS = (
        ANOTHER.CONFIG_SELECT, MAIN.NAME, DISPERSION.NAME, CAROUSEL.NAME, EFFECTS.NAME, DEBUG_PANEL.NAME,
        BATTLE_TIMER.NAME, CLOCK.NAME, HP_BARS.NAME, ARMOR_CALC.NAME, DAMAGE_LOG.GLOBAL,
        DAMAGE_LOG.TOP_LOG, DAMAGE_LOG.DONE_EXTENDED, DAMAGE_LOG.RECEIVED_EXTENDED, MAIN_GUN.NAME, TEAM_BASES.NAME,
        VEHICLE_TYPES.NAME, PANELS.PANELS_NAME, SNIPER.NAME, ARCADE.NAME, STRATEGIC.NAME, FLIGHT_TIME.NAME,
        SAVE_SHOOT.NAME, MINIMAP.NAME, ANOTHER.SHADOW_SETTINGS, SIXTH_SENSE.NAME, COLORS.NAME, SERVICE_CHANNEL.NAME
    )
    HANDLER_VALUES = {
        SNIPER.NAME: {
            'dynamic_zoom*enabled': (
                'dynamic_zoom*steps_only',
                'dynamic_zoom*zoomXMeters'
            ),
            'zoomSteps*enabled': ('zoomSteps*steps',),
            SNIPER.DISABLE_SNIPER: (SNIPER.SKIP_CLIP, SNIPER.DISABLE_LATENCY)
        },
        TEAM_BASES.NAME: {
            'outline*enabled': ('outline*color',)
        },
        PANELS.PANELS_NAME: {
            "players_bars_enabled": (
                "players_bars_settings*players_bars_bar*outline*enabled",
                "players_bars_settings*players_bars_bar*outline*customColor",
                "players_bars_settings*players_bars_bar*outline*color",
                "players_bars_settings*players_bars_bar*outline*alpha",
                "players_bars_hotkey",
                "players_bars_classColor",
                "players_bars_on_key_pressed",
            ),
            'players_bars_settings*players_bars_bar*outline*customColor': (
                'players_bars_settings*players_bars_bar*outline*color',
            ),
            'players_bars_settings*players_bars_bar*outline*enabled': (
                'players_bars_settings*players_bars_bar*outline*color',
                'players_bars_settings*players_bars_bar*outline*alpha',
                'players_bars_settings*players_bars_bar*outline*customColor'
            ),
            'players_damages_enabled': (
                'players_damages_hotkey', 'players_damages_settings*x', 'players_damages_settings*y'
            ),
            "panels_icon_enabled": ("panels_icon_filter_strength",)
        },
        ARMOR_CALC.NAME: {
            'showCalcPoints': ('calcPosition*x', 'calcPosition*y', 'template')
        },
        MAIN.NAME: {
            MAIN.ENABLE_FPS_LIMITER: (MAIN.MAX_FRAME_RATE,),
            MAIN.SHOW_ANONYMOUS: (MAIN.CHANGE_ANONYMOUS_NAME,)
        },
        HP_BARS.NAME: {
            'outline*enabled': ('outline*color',),
            'markers*enabled': ("markers*x", "markers*y", "markers*showMarkers_hotkey", "markers*markersClassColor")
        },
        MINIMAP.NAME: {
            'zoom*enabled': ('zoom*zoom_hotkey', 'zoom*indent'),
            MINIMAP.DEATH_PERMANENT: (MINIMAP.SHOW_NAMES,)
        },
        DEBUG_PANEL.NAME: {
            'debugGraphics*enabled': (
                'debugGraphics*pingBar*enabled', 'debugGraphics*fpsBar*enabled', 'debugGraphics*pingBar*color',
                'debugGraphics*fpsBar*color')
        },
        CLOCK.NAME: {
            'hangar*enabled': ('hangar*format', 'hangar*x', 'hangar*y'),
            'battle*enabled': ('battle*format', 'battle*x', 'battle*y')
        },
        SIXTH_SENSE.NAME: {
            SIXTH_SENSE.SHOW_TIMER: (SIXTH_SENSE.PLAY_TICK_SOUND,)
        },
        "reversed_values": {PANELS.BAR_CLASS_COLOR},
        DISPERSION.NAME: {
            DISPERSION.TIMER_ENABLED: (DISPERSION.TIMER_REGULAR_TEMPLATE,
                                       DISPERSION.TIMER_DONE_TEMPLATE,
                                       DISPERSION.TIMER_DONE_COLOR,
                                       DISPERSION.TIMER_COLOR,
                                       DISPERSION.TIMER_POSITION_X,
                                       DISPERSION.TIMER_POSITION_Y,
                                       DISPERSION.TIMER_ALIGN),
            DISPERSION.ENABLED: (DISPERSION.CIRCLE_SCALE_CONFIG,
                                 DISPERSION.CIRCLE_EXTRA_LAP,
                                 DISPERSION.CIRCLE_REPLACE)
        }
    }


ALIAS_TO_PATH = {
    ALIASES.HP_BARS: ".teams_hp",
    ALIASES.DAMAGE_LOG: ".damage_log",
    ALIASES.MAIN_GUN: ".main_gun",
    ALIASES.DEBUG: ".debug_panel",
    ALIASES.TIMER: ".battle_timer",
    ALIASES.SIXTH_SENSE: ".sixth_sense",
    ALIASES.TEAM_BASES: ".team_bases",
    ALIASES.ARMOR_CALC: ".armor_calculator",
    ALIASES.FLIGHT_TIME: ".flight_time",
    ALIASES.DISPERSION_TIMER: ".dispersion_timer",
    ALIASES.PANELS: ".players_panels",
    ALIASES.MINIMAP: ".minimap",
    ALIASES.USER_BACKGROUND: ".user_background",
    ALIASES.WG_COMP: ".wg_comp_settings",
    ALIASES.DATE_TIME: ".date_times"
}

ALIAS_TO_CONFIG_NAME = {
    ALIASES.HP_BARS: HP_BARS.NAME,
    ALIASES.DAMAGE_LOG: DAMAGE_LOG.NAME,
    ALIASES.MAIN_GUN: MAIN_GUN.NAME,
    ALIASES.DEBUG: DEBUG_PANEL.NAME,
    ALIASES.TIMER: BATTLE_TIMER.NAME,
    ALIASES.SIXTH_SENSE: SIXTH_SENSE.NAME,
    ALIASES.TEAM_BASES: TEAM_BASES.NAME,
    ALIASES.ARMOR_CALC: ARMOR_CALC.NAME,
    ALIASES.FLIGHT_TIME: FLIGHT_TIME.NAME,
    ALIASES.DISPERSION_TIMER: DISPERSION.NAME,
    ALIASES.PANELS: PANELS.PANELS_NAME,
    ALIASES.MINIMAP: MINIMAP.NAME,
    ALIASES.USER_BACKGROUND: USER_BACKGROUND.NAME,
    ALIASES.DATE_TIME: CLOCK.NAME,
    ALIASES.WG_COMP: MAIN.NAME
}

SORTED_ALIASES = (
    ALIASES.WG_COMP, ALIASES.MAIN_GUN, ALIASES.HP_BARS, ALIASES.DAMAGE_LOG, ALIASES.DEBUG, ALIASES.TIMER,
    ALIASES.SIXTH_SENSE, ALIASES.TEAM_BASES, ALIASES.ARMOR_CALC, ALIASES.FLIGHT_TIME, ALIASES.DISPERSION_TIMER,
    ALIASES.PANELS, ALIASES.MINIMAP, ALIASES.DATE_TIME, ALIASES.USER_BACKGROUND
)