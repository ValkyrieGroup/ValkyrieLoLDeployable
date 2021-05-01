from valkyrie import *			
from time import time
from helpers.targeting import TargetSelector, TargetSet
from helpers.flags import Orbwalker
from helpers.damages import calculate_raw_spell_dmg

import helpers.templates as HT
from helpers.spells import SpellRotation, RSpell, Slot, SpellCondition

cassiopeia = HT.ChampionScript(
	passive_trigger   = HT.Enabler.default(),
	combat_distance   = 900,
	passive_distance  = 900,
	
	combat_rotation = SpellRotation([
		RSpell(Slot.R, HT.ConditionInFrontOfTarget()), 
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
		RSpell(Slot.Q),
		RSpell(Slot.W),
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
	