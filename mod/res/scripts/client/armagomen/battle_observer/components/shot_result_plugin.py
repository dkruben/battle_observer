from AvatarInputHandler.gun_marker_ctrl import _CrosshairShotResults
from DestructibleEntity import DestructibleEntity
from Vehicle import Vehicle
from aih_constants import SHOT_RESULT
from armagomen.battle_observer.settings.default_settings import settings
from armagomen.constants import GLOBAL, ARMOR_CALC
from armagomen.utils.common import getPlayer, overrideMethod
from armagomen.utils.events import g_events
from constants import SHELL_MECHANICS_TYPE, SHELL_TYPES as SHELLS, SHELL_TYPES
from gui.Scaleform.daapi.view.battle.shared.crosshair import plugins
from gui.Scaleform.genConsts.CROSSHAIR_VIEW_ID import CROSSHAIR_VIEW_ID
from items.components.component_constants import MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS

UNDEFINED_RESULT = (SHOT_RESULT.UNDEFINED, None, None, None, False, False)
_MIN_PIERCING_DIST = 100.0
_JET_FACTOR = 0.001
_LERP_RANGE_PIERCING_DIST = 400.0
FULL_PP_RANGE = (SHELLS.HIGH_EXPLOSIVE, SHELLS.HOLLOW_CHARGE)


class _ShotResult(object):

    @staticmethod
    def isAlly(entity, player, onAlly):
        return False if onAlly else entity.publicInfo['team'] == player.team

    @classmethod
    def getShotResult(cls, hitPoint, collision, direction, piercingMultiplier, onAlly):
        if collision is None:
            return UNDEFINED_RESULT
        entity = collision.entity
        if not isinstance(entity, (Vehicle, DestructibleEntity)) or not entity.isAlive():
            return UNDEFINED_RESULT
        player = getPlayer()
        if player is None or cls.isAlly(entity, player, onAlly):
            return UNDEFINED_RESULT
        c_details = _CrosshairShotResults._getAllCollisionDetails(hitPoint, direction, entity)
        if c_details is None:
            return UNDEFINED_RESULT
        shot = player.getVehicleDescriptor().shot
        shell = shot.shell
        full_piercing_power = cls.getFullPiercingPower(hitPoint, piercingMultiplier, shot, player)
        is_modern = cls.isModernMechanics(shell)
        armor, piercing_power, ricochet, no_damage = cls.computeArmor(c_details, shell, full_piercing_power, is_modern)
        if no_damage or ricochet:
            shot_result = SHOT_RESULT.NOT_PIERCED
        else:
            offset = piercing_power * shell.piercingPowerRandomization
            if armor < piercing_power - offset:
                shot_result = SHOT_RESULT.GREAT_PIERCED
            elif armor > piercing_power + offset:
                shot_result = SHOT_RESULT.NOT_PIERCED
            else:
                shot_result = SHOT_RESULT.LITTLE_PIERCED
        if is_modern:
            piercing_power = full_piercing_power
        return shot_result, armor, piercing_power, shell.caliber, ricochet, no_damage

    @staticmethod
    def getFullPiercingPower(hitPoint, piercingMultiplier, shot, player):
        p100, p500 = (pp * piercingMultiplier for pp in shot.piercingPower)
        if shot.shell.kind in FULL_PP_RANGE:
            return p100
        else:
            distance = hitPoint.distTo(player.position)
            if distance <= _MIN_PIERCING_DIST:
                return p100
            elif distance < shot.maxDistance:
                return p100 - (p100 - p500) * (distance - _MIN_PIERCING_DIST) / _LERP_RANGE_PIERCING_DIST
            return p500

    @staticmethod
    def isModernMechanics(shell):
        return shell.kind == SHELL_TYPES.HIGH_EXPLOSIVE and shell.type.mechanics == SHELL_MECHANICS_TYPE.MODERN and \
            shell.type.shieldPenetration

    @staticmethod
    def computeArmor(c_details, shell, piercing_power, is_modern_he):
        computed_armor = GLOBAL.ZERO
        ricochet = False
        no_damage = True
        is_jet = False
        jet_start_dist = GLOBAL.ZERO
        jet_loss = _CrosshairShotResults._SHELL_EXTRA_DATA[shell.kind].jetLossPPByDist
        for detail in c_details:
            mat_info = detail.matInfo
            if mat_info is None:
                continue
            computed_armor += _CrosshairShotResults._computePenetrationArmor(shell, detail.hitAngleCos, mat_info)
            if is_jet:
                jetDist = detail.dist - jet_start_dist
                if jetDist > GLOBAL.ZERO:
                    piercing_power *= 1.0 - jetDist * jet_loss
            else:
                ricochet = _CrosshairShotResults._shouldRicochet(shell, detail.hitAngleCos, mat_info)
            if mat_info.vehicleDamageFactor:
                no_damage = False
                break
            elif is_modern_he:
                piercing_power -= computed_armor * MODERN_HE_PIERCING_POWER_REDUCTION_FACTOR_FOR_SHIELDS
            elif jet_loss > GLOBAL.ZERO:
                is_jet = True
                jet_start_dist += detail.dist + mat_info.armor * _JET_FACTOR
        return computed_armor, piercing_power, ricochet, no_damage


class ShotResultIndicatorPlugin(plugins.ShotResultIndicatorPlugin):

    def __init__(self, parentObj):
        super(ShotResultIndicatorPlugin, self).__init__(parentObj)
        self.__onAlly = bool(settings.armor_calculator[ARMOR_CALC.ON_ALLY])

    def __updateColor(self, markerType, hitPoint, collision, direction):
        shot_result, armor, piercing_power, caliber, ricochet, no_damage = \
            _ShotResult.getShotResult(hitPoint, collision, direction, self.__piercingMultiplier, self.__onAlly)
        if shot_result in self.__colors:
            color = self.__colors[shot_result]
            if self.__cache[markerType] != shot_result and self._parentObj.setGunMarkerColor(markerType, color):
                self.__cache[markerType] = shot_result
                g_events.onMarkerColorChanged(color)
            g_events.onArmorChanged(armor, piercing_power, caliber, ricochet, no_damage)

    def __setMapping(self, keys):
        super(ShotResultIndicatorPlugin, self).__setMapping(keys)
        self.__mapping[CROSSHAIR_VIEW_ID.STRATEGIC] = True


@overrideMethod(plugins, 'createPlugins')
def createPlugins(base, *args):
    _plugins = base(*args)
    if settings.armor_calculator[GLOBAL.ENABLED]:
        _plugins['shotResultIndicator'] = ShotResultIndicatorPlugin
    return _plugins
