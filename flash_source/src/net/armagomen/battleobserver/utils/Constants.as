package net.armagomen.battleobserver.utils
{
	import flash.filters.*;
	import flash.text.TextFormat;
	
	public class Constants
	{
		public static const glowScore:GlowFilter    = new GlowFilter(0, 0.9, 4, 4, 2, BitmapFilterQuality.MEDIUM, false, false);
		public static const middleText:TextFormat   = new TextFormat("$TitleFont", 18, 0xFFFFFF);
		public static const diff:TextFormat         = new TextFormat("$TitleFont", 14, 0xFFFFFF);
		public static const largeText:TextFormat    = new TextFormat("$TitleFont", 20, 0xFFFFFF);
		public static const normalText:TextFormat   = new TextFormat("$FieldFont", 16, 0xFFFFFF);
		public static const normalText15:TextFormat = new TextFormat("$FieldFont", 15, 0xFFFFFF);
		public static const scoreformat:TextFormat  = new TextFormat("$TitleFont", 24, 0xFFFFFF, true);
		public static const armorText:TextFormat    = new TextFormat("$TitleFont", 20, 0xFFFFFF, null, null, null, null, null, 'center');
		
		public static const ALPHA:Number            = 0.6;
		public static const BG_ALPHA:Number         = 0.4;
		
		public function Constants()
		{
			super();
		}
	}
}