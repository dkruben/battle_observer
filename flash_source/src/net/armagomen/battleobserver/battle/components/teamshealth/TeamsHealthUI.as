package net.armagomen.battleobserver.battle.components.teamshealth
{
	import flash.events.Event;
	import net.armagomen.battleobserver.battle.base.ObserverBattleDisplayable;
	import net.armagomen.battleobserver.battle.interfaces.ITeamHealth;
	import net.wg.data.constants.generated.BATTLE_VIEW_ALIASES;
	
	public class TeamsHealthUI extends ObserverBattleDisplayable
	{
		private var hpBars:ITeamHealth;
		private var removed:Boolean = false;
		private var correlation:* = null;
		
		public function TeamsHealthUI()
		{
			super();
		}
		
		override protected function onPopulate():void
		{
			super.onPopulate();
			this.removed = false;
			var settings:Object = this.getSettings();
			this.x = App.appWidth >> 1;
			
			if (settings.style == "league")
			{
				this.hpBars = this.addChild(new League(this.isColorBlind(), this.getColors().global)) as ITeamHealth;
			}
			else
			{
				this.hpBars = this.addChild(new Default(this.isColorBlind(), this.getColors().global)) as ITeamHealth;
			}
			var page:*       = parent;
			this.correlation = page.getComponent(BATTLE_VIEW_ALIASES.FRAG_CORRELATION_BAR);
			this.correlation.y = 20;
			this.updateCorrelationBar();
		}
		
		private function updateCorrelationBar():void
		{
			if (!this.removed)
			{
				this.correlation.removeChild(this.correlation.getChildAt(0));
				this.correlation.removeChild(this.correlation.greenBackground);
				this.correlation.removeChild(this.correlation.redBackground);
				this.correlation.removeChild(this.correlation.purpleBackground);
				this.correlation.removeChild(this.correlation.teamFragsSeparatorField);
				this.correlation.removeChild(this.correlation.allyTeamFragsField);
				this.correlation.removeChild(this.correlation.enemyTeamFragsField);
				this.correlation.removeChild(this.correlation.allyTeamHealthBar);
				this.correlation.removeChild(this.correlation.enemyTeamHealthBar);
				this.removed = true;
			}
		}
		
		public function as_updateCountersPosition():void
		{
			this.correlation.allyVehicleMarkersList._markerStartPosition = -31;
			this.correlation.enemyVehicleMarkersList._markerStartPosition = 1;
			this.correlation.allyVehicleMarkersList.sort();
			this.correlation.enemyVehicleMarkersList.sort();
		}
		
		override protected function onBeforeDispose():void
		{
			super.onBeforeDispose();
			this.hpBars.remove();
			this.hpBars = null;
			this.removed = false;
			this.correlation = null;
		}
		
		public function as_colorBlind(enabled:Boolean):void
		{
			this.hpBars.setColorBlind(enabled);
		}
		
		public function as_updateHealth(alliesHP:int, enemiesHP:int, totalAlliesHP:int, totalEnemiesHP:int):void
		{
			this.hpBars.update(alliesHP, enemiesHP, totalAlliesHP, totalEnemiesHP);
		}
		
		public function as_updateScore(ally:int, enemy:int):void
		{
			this.hpBars.updateScore(ally, enemy);
		}
		
		override public function onResizeHandle(event:Event):void
		{
			this.x = App.appWidth >> 1;
		}
	}
}