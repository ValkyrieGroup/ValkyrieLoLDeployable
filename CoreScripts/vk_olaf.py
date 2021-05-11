from valkyrie import *
from helpers.targeting import TargetSelector, TargetSet

import helpers.templates as HT
from   helpers.spells import SpellRotation, RSpell, Slot, SpellCondition, CCType
		
olaf = HT.ChampionScript(
	passive_trigger = HT.Enabler.default(),
	combat_rotation = SpellRotation([
		RSpell(Slot.E),
		RSpell(Slot.Q), 
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
					 
def valkyrie_menu(ctx: Context) :		 
	ui = ctx.ui
	olaf.ui(ctx)
								 
def valkyrie_on_load(ctx: Context) :
	global olaf
	cfg = ctx.cfg				 
	olaf = HT.ChampionScript.from_str(cfg.get_str('olaf', str(olaf)))						 
								 
def valkyrie_on_save(ctx: Context) :	 
	cfg = ctx.cfg				 
	cfg.set_str('olaf', str(olaf))
								 
def valkyrie_exec(ctx: Context) :	     
	if not ctx.player.dead:
		olaf.exec(ctx)						 
								 
