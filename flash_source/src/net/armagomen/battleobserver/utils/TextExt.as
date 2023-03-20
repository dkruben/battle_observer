﻿package net.armagomen.battleobserver.utils
{
	import flash.filters.BitmapFilterQuality;
	import flash.filters.GlowFilter;
	import flash.text.*;
	import net.armagomen.battleobserver.utils.Filters;

	public class TextExt extends TextField
	{
		public function TextExt(x:Number, y:Number, style:TextFormat, align:String, shadowSettings:Object, ui:*, enabled:Boolean=true)
		{
			super();
			if (style == null){
				style = Filters.normalText;
			}
			this.x = x;
			this.y = y;
			this.width = 1;
			this.defaultTextFormat = style;
			this.antiAliasType = AntiAliasType.ADVANCED;
			this.thickness = 200;
			this.sharpness = 200;
			this.autoSize = align;
			this.filters = [new GlowFilter(Utils.colorConvert(shadowSettings.color), shadowSettings.alpha, shadowSettings.blurX, shadowSettings.blurY, shadowSettings.strength, BitmapFilterQuality.LOW, shadowSettings.inner, shadowSettings.knockout)];
			this.selectable = false;
			this.multiline = true;
			this.visible = enabled;
			this.htmlText = "";
			ui.addChild(this);
		}
	}
}