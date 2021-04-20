from valkyrie import *
from helpers.targeting import TargetSelector, TargetSet

import helpers.templates as HT
from   helpers.spells import SpellRotation, RSpell, Slot, SpellCondition, CCType

class ConditionBehindTarget(SpellCondition):
	def _check(self, ctx, player, target, spell):
		return not player.in_front_of(target)
		
	def _get_name(self):
		return 'Player in behind of target'
	
	def _get_help(self):
		return 'Triggers when player is in behind of target'

class OlafQPredictor:
	def _predict(self, ctx, player, target, spell):
		if spell.name == 'olafaxethrowcast':
			return target.pos + (target.dir * 300)
		else:
			return ctx.predict_cast_point(player, target, spell)		
olaf = HT.ChampionScript(
	passive_trigger = HT.Enabler.default(),
	combat_rotation = SpellRotation([
		RSpell(Slot.E),
		RSpell(Slot.Q,
                       HT.ConditionInFrontOfTarget()),
		RSpell(Slot.Q,
                       ConditionBehindTarget(), predictor = OlafQPredictor()), 
		RSpell(Slot.W,
			HT.ConditionDistanceToTarget(0.0, 500.0)
		),
		RSpell(Slot.R, 
			HT.ConditionCC(CCType.Stun, HT.ConditionCC.Me)
		)
	]),
	lasthit_rotation = SpellRotation([
		RSpell(Slot.Q, HT.ConditionKillable()),
		RSpell(Slot.E, HT.ConditionKillable())
	]),
	lanepush_rotation = SpellRotation([
		RSpell(Slot.Q),
		RSpell(Slot.E, HT.ConditionKillable())
	]),
	passive_rotation = SpellRotation([
		RSpell(Slot.Q)
	])
)
					 
def valkyrie_menu(ctx) :		 
	ui = ctx.ui
	olaf.ui(ctx)
								 
def valkyrie_on_load(ctx) :	 
	global olaf
	cfg = ctx.cfg				 
	olaf = HT.ChampionScript.from_str(cfg.get_str('olaf', str(olaf)))						 
								 
def valkyrie_on_save(ctx) :	 
	cfg = ctx.cfg				 
	cfg.set_str('olaf', str(olaf))
								 
def valkyrie_exec(ctx) :	     
	if not ctx.player.dead:
		olaf.exec(ctx)						 
								 
