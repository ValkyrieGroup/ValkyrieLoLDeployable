from valkyrie import *
from time import time
from helpers.targeting import TargetSelector, TargetSet
from helpers.flags import Orbwalker
from helpers.damages import calculate_raw_spell_dmg

import helpers.templates as HT
from helpers.spells import SpellRotation, RSpell, Slot, SpellCondition

class ConditionAnnieR(SpellCondition):

	def __init__(self):
		self.enabled = True
		
	def _ui(self, ctx, ui):
		pass
		
	def _check(self, ctx, player, target, spell):
		if player.has_buff('AnnieRController'):
			return False
			
		return True
		
	def _get_name(self):
		return 'Annie Smart Ultimate'
		
	def _get_help(self):
		return 'Condition for annie smart ult'

class ConditionHasAnnieStun(SpellCondition):

	def __init__(self):
		self.enabled = True
		
	def _ui(self, ctx, ui):
		pass
		
	def _check(self, ctx, player, target, spell):
		return player.has_buff('anniepassiveprimed')
		
	def _get_name(self):
		return 'Has Annie Stun'
		
	def _get_help(self):
		return 'Triggers when annie has her stun'

annie = HT.ChampionScript(
    passive_trigger   = HT.Enabler.default(),
	
	combat_rotation = SpellRotation([
        RSpell(Slot.Q),
		RSpell(Slot.W),
        RSpell(Slot.R, 
			HT.MixedConditions([ConditionAnnieR(), ConditionHasAnnieStun()], HT.MixedConditions.All),
			predictor = HT.ClusterSpellPredictor(1)),
	]),
		
	passive_rotation = SpellRotation([
		RSpell(Slot.Q)
	]),
	
	lasthit_rotation = SpellRotation([
		RSpell(Slot.Q, HT.ConditionKillable())
	]),
	
	lanepush_rotation = SpellRotation([
		RSpell(Slot.Q),
        RSpell(Slot.W, predictor = HT.ClusterSpellPredictor(3))
	])
)

def valkyrie_menu(ctx: Context) :		 
	global annie
	ui = ctx.ui
	
	annie.ui(ctx)
	
def valkyrie_menu(ctx: Context) :	 
	global annie
	cfg = ctx.cfg
	
	annie = HT.ChampionScript.from_str(cfg.get_str('annie', str(annie)))

def valkyrie_on_save(ctx: Context) :	 
	cfg = ctx.cfg

	cfg.set_str('annie', str(annie))
	
def valkyrie_exec(ctx: Context) :
	annie.exec(ctx)
