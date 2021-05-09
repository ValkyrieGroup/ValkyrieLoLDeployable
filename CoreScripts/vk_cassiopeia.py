from valkyrie import *			
from time import time
from helpers.targeting import TargetSelector, TargetSet
from helpers.flags import Orbwalker
from helpers.damages import calculate_raw_spell_dmg

import helpers.templates as HT
from helpers.spells import SpellRotation, RSpell, Slot, SpellCondition

cassiopeia = HT.ChampionScript(
	passive_trigger   = HT.Enabler.default(),
	
	combat_rotation = SpellRotation([
		RSpell(Slot.R, 
			HT.MixedConditions([HT.ConditionInFrontOfTarget(), HT.ConditionDistanceToTarget(0.0, 700.0)], HT.MixedConditions.All)
		), 
		RSpell(Slot.W), 
		RSpell(Slot.Q), 
		RSpell(Slot.E)
	]),

	passive_rotation = SpellRotation([
		RSpell(Slot.Q), 
		RSpell(Slot.E, HT.ConditionTargetPoisoned())
	]),
	
	lasthit_rotation = SpellRotation([
		RSpell(Slot.E, HT.ConditionKillable())
	]),
	
	lanepush_rotation = SpellRotation([
		RSpell(Slot.Q, predictor = HT.ClusterSpellPredictor(2)),
		RSpell(Slot.W, predictor = HT.ClusterSpellPredictor(3)),
		RSpell(Slot.E)
	]),
)

last_hit_e = True

def valkyrie_menu(ctx) :		 
	global cassiopeia, last_hit_e
	ui = ctx.ui					 
	
	cassiopeia.ui(ctx)
	
def valkyrie_on_load(ctx) :	 
	global cassiopeia, last_hit_e
	cfg = ctx.cfg				 
	
	cassiopeia = HT.ChampionScript.from_str(cfg.get_str('cassiopeia', str(cassiopeia)))
	
	
def valkyrie_on_save(ctx) :	 
	cfg = ctx.cfg				 
	
	cfg.set_str('cassiopeia', str(cassiopeia))
	
def valkyrie_exec(ctx) :	     
	
	if ctx.player.dead:
		return
		
	cassiopeia.exec(ctx)
	