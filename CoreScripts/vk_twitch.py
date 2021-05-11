from valkyrie import *
from helpers.spells import Slot
from helpers.damages import calculate_raw_spell_dmg

auto_e_killable = True
collector_id = 6676

def calc_collector_dmg(player):
	return player.health * 0.05

def valkyrie_menu(ctx: Context) :
	global auto_e_killable, draw_e_indicator
	ui = ctx.ui	
	
	auto_e_killable = ui.checkbox('Auto E when killable', auto_e_killable)
	
def valkyrie_menu(ctx: Context) :	 
	global auto_e_killable, draw_e_indicator
	cfg = ctx.cfg				 
	
	auto_e_killable = cfg.get_bool('auto_e_killable', auto_e_killable)
	
def valkyrie_on_save(ctx: Context) :	 
	cfg = ctx.cfg				 
	
	cfg.set_bool('auto_e_killable', auto_e_killable)
	
def valkyrie_exec(ctx: Context) :
	player = ctx.player

	if not auto_e_killable or player.dead:
		return

	spell = player.spells[Slot.E]
	if not player.can_cast_spell(spell):
		return
	
	has_collector = False
	for val in player.item_slots:
		if val.item and val.item.id == collector_id:
			has_collector = True
			break
	
	raw_dmg = calculate_raw_spell_dmg(player, spell)
	collector_dmg = 0
	 
	for champ in ctx.champs.enemy_to(player).targetable().near(player, 1200.0).get():
		if has_collector:
			collector_dmg = calc_collector_dmg(champ)

		if champ.health - raw_dmg.calc_against(ctx, player, champ) - collector_dmg <= 0.0:
			ctx.cast_spell(spell, None)
			break