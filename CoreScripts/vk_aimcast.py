from valkyrie import *			 
from helpers.targeting import TargetSelector, TargetSet
from helpers.templates import Enabler
from helpers.inputs    import KeyInput
import json

keys = [
	True, True, True, True, True, True
]

keybinds = {
	0: lambda ctx: ctx.keybinds.cast_q,
	1: lambda ctx: ctx.keybinds.cast_w,
	2: lambda ctx: ctx.keybinds.cast_e,
	3: lambda ctx: ctx.keybinds.cast_r,
	4: lambda ctx: ctx.keybinds.cast_d,
	5: lambda ctx: ctx.keybinds.cast_f
}

channels = [
	False, False, False, False
]

col_pill = Col(0.3, 0.9, 0.9, 0.9)
enabler  = Enabler()

target_sel = TargetSelector(0, TargetSet.Champion)
target_minions  = False
target_monsters = True
no_aim_when_no_target = False


def update_keys(ctx):
	for i, val in enumerate(keys):
		ctx.set_key_active(keybinds[i](ctx), False if val else True)
		
def valkyrie_menu(ctx):
	global target_minions, target_monsters, no_aim_when_no_target
	ui = ctx.ui
	
	target_sel.ui('Target selector', ctx, ui)
	target_minions = ui.checkbox('Target minions', target_minions)
	target_monsters = ui.checkbox('Target jungle monsters', target_monsters)
	no_aim_when_no_target = ui.checkbox('Cast normally if there is no target', no_aim_when_no_target)
	
	ui.separator()
	keys[0] = ui.checkbox('Auto aim Q', keys[0])
	keys[1] = ui.checkbox('Auto aim W', keys[1])
	keys[2] = ui.checkbox('Auto aim E', keys[2])
	keys[3] = ui.checkbox('Auto aim R', keys[3])
	keys[4] = ui.checkbox('Auto aim summoner D', keys[4])
	keys[5] = ui.checkbox('Auto aim summoner F', keys[5])
	update_keys(ctx)
	
	ui.separator()
	enabler.ui(ui)
	
	ui.text("Some champions arent tested yet (please report spells without prediction)", Col.Red)
	
def valkyrie_on_load(ctx) :	
	global keys, target_sel, enabler
	global target_minions, target_monsters, no_aim_when_no_target
	cfg = ctx.cfg				 
	
	keys = json.loads(cfg.get_str('keys', json.dumps(keys)))
	update_keys(ctx)
	
	target_sel            = TargetSelector.from_str(cfg.get_str('target_sel', str(target_sel)))
	target_minions        = cfg.get_bool('target_minions', target_minions)
	target_monsters       = cfg.get_bool('target_monsters', target_monsters)
	no_aim_when_no_target = cfg.get_bool('no_aim_when_no_target', no_aim_when_no_target)
	enabler               = Enabler.from_str(cfg.get_str('enabler', str(enabler)))
	
def valkyrie_on_save(ctx) :	 
	cfg = ctx.cfg				 
	
	cfg.set_str('keys', json.dumps(keys))
	cfg.set_str('target_sel', str(target_sel))
	cfg.set_bool('target_minions', target_minions)
	cfg.set_bool('target_monsters', target_monsters)
	cfg.set_bool('no_aim_when_no_target', no_aim_when_no_target)
	cfg.set_str('enabler', str(enabler))
	
def cast(ctx, spell, static, end_channel = False):
		
	if static.has_flag(Spell.DashSkill) or static.has_flag(Spell.CastAnywhere):
		ctx.cast_spell(spell, None)
		return
	
	player = ctx.player
	type_hover = type(ctx.hovered)
	target = None
	if (type_hover == MinionObj or type_hover == ChampionObj) and ctx.hovered.team != player.team:
		target = ctx.hovered
	else:
		target = target_sel.get_target(ctx, ctx.champs.enemy_to(player).targetable().near(player, static.cast_range).get())
		if not target and target_minions:
			target = target_sel.get_target(ctx, ctx.minions.enemy_to(player).targetable().near(player, static.cast_range).get())
		if not target and target_monsters:
			target = target_sel.get_target(ctx, ctx.jungle.enemy_to(player).targetable().near(player, static.cast_range).get())
	
	point = None
	if target:
		point = ctx.predict_cast_point(player, target, spell)
	
	if not point and not no_aim_when_no_target:
		return
		
	if end_channel:
		ctx.end_channel(spell, point)
	else:
		ctx.cast_spell(spell, point)
	
def valkyrie_exec(ctx) :	     
	global channels
	
	if enabler.check(ctx):
		ctx.pill('Aimcast', Col.Black, col_pill)
	else:
		return
		
	spells = ctx.player.spells
	for i in range(len(keys)):
		if not keys[i]:
			continue
			
		key = keybinds[i](ctx)
		
		spell = spells[i]
		static = spell.static
		if static == None:
			continue
		
		is_channel = static.has_flag(Spell.ChargeableSkill)
		
		if is_channel:
			if ctx.was_pressed(key):
				if channels[i]:
					cast(ctx, spell, static, True)
					channels[i] = False
				else:
					channels[i] = ctx.start_channel(spell)
		
		elif ctx.was_pressed(key):
			cast(ctx, spell, static)
			
	 
	
