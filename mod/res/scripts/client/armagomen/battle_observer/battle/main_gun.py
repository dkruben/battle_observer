from collections import defaultdict
from math import ceil

from armagomen.battle_observer.meta.battle.main_gun_meta import MainGunMeta
from armagomen.constants import MAIN_GUN, GLOBAL, POSTMORTEM
from armagomen.utils.common import logDebug
from gui.battle_control import avatar_getter
from gui.battle_control.controllers.battle_field_ctrl import IBattleFieldListener


class MainGun(MainGunMeta, IBattleFieldListener):

    def __init__(self):
        super(MainGun, self).__init__()
        self.macros = defaultdict(lambda: GLOBAL.CONFIG_ERROR)
        self.gunScore = GLOBAL.ZERO
        self.gunLeft = GLOBAL.ZERO
        self.enemiesHP = GLOBAL.ZERO
        self.playerDead = False
        self.totalEnemiesHP = GLOBAL.ZERO
        self.playersDamage = defaultdict(int)

    def onEnterBattlePage(self):
        super(MainGun, self).onEnterBattlePage()
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleHealthChanged += self.onPlayersDamaged

    def onExitBattlePage(self):
        handler = avatar_getter.getInputHandler()
        if handler is not None and hasattr(handler, "onCameraChanged"):
            handler.onCameraChanged += self.onCameraChanged
        arena = self._arenaVisitor.getArenaSubscription()
        if arena is not None:
            arena.onVehicleHealthChanged -= self.onPlayersDamaged
        super(MainGun, self).onExitBattlePage()

    def _populate(self):
        super(MainGun, self)._populate()
        self.macros.update(mainGunIcon=self.settings[MAIN_GUN.GUN_ICON],
                           mainGunColor=self.colors[MAIN_GUN.NAME][MAIN_GUN.COLOR],
                           mainGunDoneIcon=GLOBAL.EMPTY_LINE, mainGunFailureIcon=GLOBAL.EMPTY_LINE)

    def updateTeamHealth(self, alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP):
        if self.enemiesHP != enemiesHP:
            self.enemiesHP = enemiesHP
            if enemiesHP < self.gunLeft:
                self.updateMainGun(criteria="low enemy health")
        if self.totalEnemiesHP != totalEnemiesHP:
            self.totalEnemiesHP = totalEnemiesHP
            self.gunScore = max(MAIN_GUN.MIN_GUN_DAMAGE, int(ceil(totalEnemiesHP * MAIN_GUN.DAMAGE_RATE)))
            self.updateMainGun(criteria="total health")

    def updateMainGun(self, criteria=None):
        playerDamage = self.playersDamage[self._player.playerVehicleID]
        maxDamage = max(self.playersDamage.itervalues())
        dealtMoreDamage = playerDamage < maxDamage > self.gunScore
        if dealtMoreDamage:
            self.gunLeft = maxDamage - playerDamage
        else:
            self.gunLeft = self.gunScore - playerDamage
        achieved = self.gunLeft <= GLOBAL.ZERO
        self.macros[MAIN_GUN.INFO] = GLOBAL.EMPTY_LINE if achieved else self.gunLeft
        self.macros[MAIN_GUN.DONE_ICON] = self.settings[MAIN_GUN.DONE_ICON] if achieved else GLOBAL.EMPTY_LINE
        if not achieved and self.enemiesHP < self.gunLeft or dealtMoreDamage:
            self.macros[MAIN_GUN.FAILURE_ICON] = self.settings[MAIN_GUN.FAILURE_ICON] + criteria
        else:
            self.macros[MAIN_GUN.FAILURE_ICON] = GLOBAL.EMPTY_LINE
        logDebug(
            "MainGun: playerDamage={}, maxDamage={}, dealtMoreDamage={}, self.gunLeft={}, achieved={}, criteria={}",
            playerDamage, maxDamage, dealtMoreDamage, self.gunLeft, achieved, criteria)
        self.as_mainGunTextS(self.settings[MAIN_GUN.TEMPLATE] % self.macros)

    def onCameraChanged(self, ctrlMode, vehicleID=None):
        self.playerDead = ctrlMode in POSTMORTEM.MODES

    def onPlayersDamaged(self, targetID, attackerID, damage):
        if self._arenaDP.isAlly(attackerID):
            self.playersDamage[attackerID] += damage
            if attackerID == self._player.playerVehicleID:
                self.updateMainGun(criteria="player damage")
