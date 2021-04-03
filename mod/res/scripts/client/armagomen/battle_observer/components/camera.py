import math

from Avatar import PlayerAvatar
from AvatarInputHandler.AimingSystems.SniperAimingSystem import SniperAimingSystem
from AvatarInputHandler.DynamicCameras.ArcadeCamera import ArcadeCamera, MinMax
from AvatarInputHandler.DynamicCameras.ArtyCamera import ArtyCamera
from AvatarInputHandler.DynamicCameras.SniperCamera import SniperCamera
from AvatarInputHandler.DynamicCameras.StrategicCamera import StrategicCamera
from AvatarInputHandler.control_modes import SniperControlMode
from PlayerEvents import g_playerEvents
from account_helpers.settings_core.options import SniperZoomSetting
from aih_constants import CTRL_MODE_NAME
from armagomen.battle_observer.core import settings
from armagomen.battle_observer.core.bo_constants import ARCADE, GLOBAL, SNIPER, STRATEGIC, MAIN
from armagomen.utils.common import overrideMethod, getPlayer, logError, vector3

SENSITIVITY = set()
g_playerEvents.onArenaCreated += SENSITIVITY.clear


@overrideMethod(SniperCamera, "create")
def sniper_create(base, camera, onChangeControlMode=None):
    if settings.zoom[GLOBAL.ENABLED]:
        if settings.zoom[SNIPER.ZOOM_STEPS][GLOBAL.ENABLED]:
            if len(settings.zoom[SNIPER.ZOOM_STEPS][SNIPER.STEPS]) > GLOBAL.TWO:
                steps = settings.zoom[SNIPER.ZOOM_STEPS][SNIPER.STEPS]
                steps.sort()
                exposure_range = xrange(len(steps) + GLOBAL.ONE, GLOBAL.ONE, -GLOBAL.ONE)
                camera._cfg[SNIPER.INCREASED_ZOOM] = True
                camera._cfg[SNIPER.ZOOMS] = steps
                camera._SniperCamera__dynamicCfg[SNIPER.ZOOM_EXPOSURE] = \
                    [round(SNIPER.EXPOSURE_FACTOR * step, GLOBAL.ONE) for step in exposure_range]
        if settings.zoom[SNIPER.DYN_ZOOM][GLOBAL.ENABLED]:
            setattr(camera, "dist_for_step", math.ceil(SNIPER.MAX_DIST / len(camera._cfg[SNIPER.ZOOMS])))
    return base(camera, onChangeControlMode=onChangeControlMode)


@overrideMethod(SniperZoomSetting, "setSystemValue")
def setSystemValue(base, zoomSettings, value):
    return base(zoomSettings, GLOBAL.ZERO if settings.zoom[SNIPER.DYN_ZOOM][GLOBAL.ENABLED] else value)


@overrideMethod(SniperCamera, "enable")
def enable(base, camera, targetPos, saveZoom):
    if settings.zoom[GLOBAL.ENABLED]:
        player = getPlayer()
        if settings.zoom[SNIPER.GUN_ZOOM]:
            targetPos = player.gunRotator.markerInfo[GLOBAL.FIRST]
        if settings.zoom[SNIPER.DYN_ZOOM][GLOBAL.ENABLED]:
            dist = int((player.getOwnVehiclePosition() - vector3(*targetPos)).length)
            if settings.zoom[SNIPER.DYN_ZOOM][SNIPER.STEPS_ONLY]:
                index = int(math.ceil(dist / camera.dist_for_step) - GLOBAL.ONE)
                camera._cfg[SNIPER.ZOOM] = camera._cfg[SNIPER.ZOOMS][index]
            else:
                maxZoom = camera._cfg[SNIPER.ZOOMS][GLOBAL.LAST]
                zoom = round(dist / settings.zoom[SNIPER.DYN_ZOOM][SNIPER.METERS])
                if zoom > maxZoom:
                    zoom = maxZoom
                camera._cfg[SNIPER.ZOOM] = zoom
    return base(camera, targetPos, saveZoom or settings.zoom[SNIPER.DYN_ZOOM][GLOBAL.ENABLED])


def changeControlMode(avatar, shooterID):
    if shooterID == avatar.playerVehicleID:
        input_handler = avatar.inputHandler
        if input_handler is not None and isinstance(input_handler.ctrl, SniperControlMode):
            if settings.zoom[SNIPER.SKIP_CLIP]:
                v_desc = avatar.getVehicleDescriptor()
                if v_desc.shot.shell.caliber < SNIPER.MAX_CALIBER or SNIPER.CLIP in v_desc.gun.tags:
                    return
            aiming_system = input_handler.ctrl.camera.aimingSystem
            input_handler.onControlModeChanged(CTRL_MODE_NAME.ARCADE,
                                               prevModeName=input_handler.ctrlModeName,
                                               preferredPos=aiming_system.getDesiredShotPoint(),
                                               turretYaw=aiming_system.turretYaw,
                                               gunPitch=aiming_system.gunPitch,
                                               aimingMode=input_handler.ctrl._aimingMode,
                                               closesDist=False)


@overrideMethod(PlayerAvatar, "showTracer")
def showTracer(base, avatar, shooterID, *args):
    try:
        if settings.zoom[SNIPER.DISABLE_SNIPER] and settings.zoom[GLOBAL.ENABLED]:
            changeControlMode(avatar, shooterID)
    except Exception as err:
        logError("I can't get out of sniper mode. Error {0}.changeControlMode, {1}".format(__package__, err))
    finally:
        return base(avatar, shooterID, *args)


@overrideMethod(ArcadeCamera, "create")
def arcade_create(base, camera, *args, **kwargs):
    if settings.arcade_camera[GLOBAL.ENABLED]:
        cfg = camera._cfg
        cfg[ARCADE.DIST_RANGE] = MinMax(settings.arcade_camera[ARCADE.MIN],
                                        settings.arcade_camera[ARCADE.MAX])
        cfg[ARCADE.START_DIST] = settings.arcade_camera[ARCADE.START_DEAD_DIST]
        cfg[ARCADE.START_ANGLE] = ARCADE.ANGLE
        if ARCADE.NAME not in SENSITIVITY:
            cfg[ARCADE.SCROLL_SENSITIVITY] *= settings.arcade_camera[ARCADE.SCROLL_MULTIPLE]
            SENSITIVITY.add(ARCADE.NAME)
    return base(camera, *args, **kwargs)


@overrideMethod(StrategicCamera, "create")
@overrideMethod(ArtyCamera, "create")
def arty_create(base, camera, *args, **kwargs):
    if settings.strategic_camera[GLOBAL.ENABLED]:
        dist_range = (settings.strategic_camera[STRATEGIC.MIN], settings.strategic_camera[STRATEGIC.MAX])
        camera._userCfg[STRATEGIC.DIST_RANGE] = dist_range
        camera._cfg[STRATEGIC.DIST_RANGE] = dist_range
        if STRATEGIC.NAME not in SENSITIVITY:
            camera._cfg[ARCADE.SCROLL_SENSITIVITY] *= settings.strategic_camera[ARCADE.SCROLL_MULTIPLE]
            camera._userCfg[ARCADE.SCROLL_SENSITIVITY] *= settings.strategic_camera[ARCADE.SCROLL_MULTIPLE]
            SENSITIVITY.add(STRATEGIC.NAME)
    return base(camera, *args, **kwargs)


@overrideMethod(SniperAimingSystem, "__isTurretHasStaticYaw")
@overrideMethod(SniperControlMode, "getPreferredAutorotationMode")
def removeHandbrake(base, *args, **kwargs):
    return settings.main[MAIN.REMOVE_HANDBRAKE] or base(*args, **kwargs)


@overrideMethod(SniperControlMode, "enable")
def sniperControlMode_enable(base, controlMode, *args, **kwargs):
    result = base(controlMode, *args, **kwargs)
    if settings.main[MAIN.REMOVE_HANDBRAKE]:
        controlMode._cam.aimingSystem.enableHorizontalStabilizerRuntime(True)
        controlMode._cam.aimingSystem.forceFullStabilization(True)
    return result
