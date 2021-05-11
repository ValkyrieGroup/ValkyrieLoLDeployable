from valkyrie import *
from time import time
from helpers.targeting import TargetSelector, TargetSet
from helpers.flags import Orbwalker
from helpers.damages import calculate_raw_spell_dmg

import helpers.templates as HT
from helpers.spells import SpellRotation, RSpell, Slot, SpellCondition

class ConditionXerathUlt(SpellCondition):

	def __init__(self):
		self.enabled = True
		self.killable = HT.ConditionKillable()
		
	def _ui(self, ctx, ui):
		pass
		
	def _check(self, ctx, player, target, spell):
		if player.spells[3].name == 'xerathlocusofpower2':
			return self.killable._check(ctx, player, target, spell)
		
		return True
		
	def _get_name(self):
		return 'Smart Ultimate'
		
	def _get_help(self):
		return 'Conditions for xerath ult'

xerath = HT.ChampionScript(
        passive_trigger   = HT.Enabler.default(),
	
	combat_rotation = SpellRotation([
        RSpell(Slot.E),
		RSpell(Slot.W),
        RSpell(Slot.Q),
        RSpell(Slot.R, ConditionXerathUlt()),
	]),
		
	passive_rotation = SpellRotation([
		RSpell(Slot.Q),
        RSpell(Slot.W),
        RSpell(Slot.E)
	]),
	
	lasthit_rotation = SpellRotation([
	]),
	
	lanepush_rotation = SpellRotation([
		RSpell(Slot.Q),
        RSpell(Slot.W, predictor = HT.ClusterSpellPredictor(3))
	])
)

def valkyrie_menu(ctx: Context) :		 
	global xerath
	ui = ctx.ui
	
	xerath.ui(ctx)
	
def valkyrie_on_load(ctx: Context) :
	global xerath
	cfg = ctx.cfg
	
	xerath = HT.ChampionScript.from_str(cfg.get_str('xerath', str(xerath)))

def valkyrie_on_save(ctx: Context) :	 
	cfg = ctx.cfg

	cfg.set_str('xerath', str(xerath))
	
def valkyrie_exec(ctx: Context) :
        
	if ctx.player.dead:
                return
		
	xerath.exec(ctx)
