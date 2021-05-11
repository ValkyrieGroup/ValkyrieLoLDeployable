from valkyrie import *
from helpers.targeting import *
from helpers.prediction import *
from helpers.drawings import Circle
from helpers.inputs import KeyInput
from helpers.spells import Buffs
from helpers.items import get_onhit_physical, get_onhit_magical
from time import time
from enum import Enum
import math
from helpers.flags import EvadeFlags, Orbwalker

dead_zone               = Circle(100.0, 50.0, 3.0, Col.Gray, True, True, 1)
target_selector         = TargetSelector(0, TargetSet.Champion)
target_selector_monster = TargetSelector(0, TargetSet.Monster)

max_atk_speed   = 5.0
key_kite		= KeyInput(Key.space, True)
key_last_hit	= KeyInput(Key.v, True)
key_lane_push   = KeyInput(Key.c, True)
move_interval   = 0.10

delay_percent = 0.115

class OrbwalkKite:
	type = Orbwalker.ModeKite
	
	def get_target(self, ctx, distance):
		possible_targets = ctx.champs.targetable().enemy_to(ctx.player).near(ctx.player, distance).get()
		return target_selector.get_target(ctx, possible_targets)

class OrbwalkLastHit:
	type = Orbwalker.ModeKite
	
	def get_target(self, ctx, distance):
		lasthits = predict_minions_lasthit(ctx, ctx.minions.alive().enemy_to(ctx.player).on_screen().get(), ctx.minions.alive().ally_to(ctx.player).on_screen().get())
		if len(lasthits) == 0:
			return None
			
		lasthits = sorted(lasthits, key = lambda p: p[0].health - p[1], reverse = True)
		for minion, predicted_hp, player_dmg in lasthits:
			if predicted_hp - math.floor(player_dmg) <= 0.0:
				return minion
			
		return None

class OrbwalkLanePush:
	type = Orbwalker.ModeKite
	allow_champ = False
	
	class LanePushInfo:
		def __init__(self, minion):
			self.minion = minion
			self.attackers = [] 
			
		def score(self, all_attackers):
			ph         = self.minion.health/self.minion.max_health
			pa         = len(self.attackers)/len(all_attackers)
			
			hp_comp  = 0.7/(1.0 + ph)
			atk_comp = 0.3*(1.0 + pa)
				
			siege_comp = 0.1 if 'siege' in self.minion.name and ph < 0.15 else 0.0
			
			return hp_comp + atk_comp + siege_comp
	
	def get_target(self, ctx, distance):
		player			  = ctx.player
		
		if self.allow_champ:
			target = kite_mode.get_target(ctx, distance)
			if target:
				return target
		
		# Try getting jungle mob
		jungle_target = target_selector_monster.get_target(ctx, ctx.jungle.targetable().enemy_to(player).near(player, distance).get())
		if jungle_target:
			return jungle_target
			
		# Minion logic
		ally_minions = ctx.minions.targetable().ally_to(player).near(player, distance).get()
		enemy_minions = ctx.minions.targetable().enemy_to(player).near(player, distance).get()
		
		# Get attackers
		minions = { m.index : self.LanePushInfo(m) for m in enemy_minions }
		for ally_m in ally_minions:
			if ally_m.curr_casting and ally_m.curr_casting.dest_index in minions:
				minions[ally_m.curr_casting.dest_index].attackers.append(ally_m)
		
		sorted_minions = sorted(minions.values(), key = lambda info: info.score(enemy_minions), reverse = True)
		if len(sorted_minions) > 0:
			best_target = sorted_minions[0]
			if len(best_target.attackers) == 0:
				return best_target.minion
			
			enemy_minion        = best_target.minion
			hit_dmg		 		= get_onhit_physical(player, enemy_minion) + get_onhit_magical(player, enemy_minion)
			
			basic_atk_speed	 = player.static.basic_atk.speed
			basic_atk_delay	 = player.static.basic_atk_windup / player.atk_speed
			t_until_player_hits = basic_atk_delay + player.pos.distance(enemy_minion.pos) / basic_atk_speed
			
			health = predict_minion_health(ctx, enemy_minion, best_target.attackers, t_until_player_hits, 0.0, MinionModifiers(ctx))
			health_perc = health/enemy_minion.max_health
			dmg_speed = (enemy_minion.health - health)/enemy_minion.max_health
			if health - hit_dmg <= 0.0:
				return enemy_minion
			else:
				possible_dmg = 0.0
				for attacker in best_target.attackers:
					possible_dmg += attacker.atk
				
				if (enemy_minion.health - possible_dmg - hit_dmg) > hit_dmg:
					return enemy_minion
		
		# Get turret / other entities
		possible_targets = ctx.turrets.targetable().enemy_to(player).near(player, distance).get() + ctx.others.targetable().enemy_to(player).near(player, distance).get()
		return target_selector.get_target(ctx, possible_targets)
		
kite_mode	    = OrbwalkKite()
last_hit_mode   = OrbwalkLastHit()
lane_push_mode  = OrbwalkLanePush()

def valkyrie_menu(ctx: Context):
	global target_selector, max_atk_speed, move_interval, delay_percent
	global key_kite, key_last_hit, key_lane_push
	ui = ctx.ui
	
	ui.text('Target Selectors', Col.Purple)
	target_selector.ui("Champion targeting", ctx, ui)
	ui.separator()
	target_selector_monster.ui('Monster targeting', ctx, ui)
	ui.separator()
	
	ui.text('Targeting', Col.Purple)
	dead_zone.ui('Orbwalker dead zone', ctx, False)
	ui.help('If mouse is within this circle the orbwalker will not issue move commands')
	lane_push_mode.allow_champ = ui.checkbox('Allow target champion while lane pushing', lane_push_mode.allow_champ)
	
	ui.separator()
	ui.text('Accuracy settings', Col.Purple)
	move_interval  = ui.sliderfloat("Move command interval (ms)", move_interval, 0.10, 0.20)
	ui.help('Cooldown for move commands, the less the more clicks you will do while moving.')
	
	delay_percent  = ui.sliderfloat('Delay percent (%)', delay_percent, 0.0, 0.4)
	ui.help('Delay percent account for lag. Usually 0.1 is a good value. You should experiment at high attack speeds with lethal tempo in a practice game.')
	
	ui.separator()
	ui.text('Key settings', Col.Purple)
	key_kite.ui("Key kite champions", ui)
	key_last_hit.ui("Key last hit minions (No Turret Farming Yet)", ui)
	key_lane_push.ui("Key lane push", ui)
	
	

def valkyrie_menu(ctx: Context):
	global target_selector, max_atk_speed, move_interval, target_selector_monster, delay_percent
	global key_kite, key_last_hit, key_lane_push, dead_zone
	cfg = ctx.cfg
	
	target_selector		      = TargetSelector.from_str(cfg.get_str("target", str(target_selector)))
	target_selector_monster   = TargetSelector.from_str(cfg.get_str("target_monster", str(target_selector_monster)))
	
	max_atk_speed   = cfg.get_float("max_atk_speed", max_atk_speed)
	move_interval   = cfg.get_float("move_interval", move_interval)
	delay_percent   = cfg.get_float("delay_percent", delay_percent)
	key_kite		= KeyInput.from_str(cfg.get_str("key_kite", str(key_kite)))
	key_last_hit	= KeyInput.from_str(cfg.get_str("key_last_hit", str(key_last_hit)))
	key_lane_push   = KeyInput.from_str(cfg.get_str("key_lane_push", str(key_lane_push)))
	lane_push_mode.allow_champ = cfg.get_bool('lane_push_mode.allow_champ', False)
	dead_zone       = Circle.from_str(cfg.get_str("dead_zone", str(dead_zone)))
	
	Orbwalker.Present = True
	Orbwalker.SelectorChampion = target_selector
	Orbwalker.SelectorMonster  = target_selector_monster
	Orbwalker.ModeKite = kite_mode
	Orbwalker.ModeLastHit = last_hit_mode
	Orbwalker.ModeLanePush = lane_push_mode
	
def valkyrie_on_save(ctx: Context):
	cfg = ctx.cfg
	
	cfg.set_str("target", str(target_selector))
	cfg.set_str("target_monster", str(target_selector_monster))
	
	cfg.set_float("delay_percent", delay_percent)
	cfg.set_float("max_atk_speed", max_atk_speed)
	cfg.set_float("move_interval", move_interval)
	cfg.set_str("key_kite", str(key_kite))
	cfg.set_str("key_last_hit", str(key_last_hit))
	cfg.set_str("key_lane_push", str(key_lane_push))
	cfg.set_bool("lane_push_mode.allow_champ", lane_push_mode.allow_champ)
	cfg.set_str("dead_zone", str(dead_zone))

last_moved	= 0
last_attacked = 0

def valkyrie_exec(ctx: Context):
	global last_moved, last_attacked
	
	Orbwalker.CurrentMode = None
	
	now = time()
	if now < Orbwalker.PauseUntil:
		return
		
	# Skip if player dead
	player = ctx.player   
	if player.dead:
		return
		
	dead_zone.draw_at(ctx, player.pos)

	# Skip if evading
	if now < EvadeFlags.EvadeEndTime:
		return
	
	if key_kite.check(ctx):
		ctx.pill('Kite', Col.Black, Col.White)
		Orbwalker.CurrentMode = kite_mode
	elif key_last_hit.check(ctx):
		ctx.pill('LastHit', Col.Black, Col.White)
		Orbwalker.CurrentMode = last_hit_mode
	elif key_lane_push.check(ctx):
		ctx.pill('LanePush', Col.Black, Col.White)
		Orbwalker.CurrentMode = lane_push_mode
	else:
		return

	has_lethal_tempo = Buffs.has_buff(player, 'LethalTempo') 
	atk_speed	     = player.atk_speed if has_lethal_tempo else min(player.atk_speed, 2.5)
	if atk_speed == 0.0:
		return
		
	c_atk_time	     = (1.0 + delay_percent)/atk_speed
	b_windup_time    = player.static.basic_atk_windup*c_atk_time						
	
	target = None
	dt = now - last_attacked
	
	if not player.channeling and dt > c_atk_time:
		target = Orbwalker.CurrentMode.get_target(ctx, player.atk_range + player.static.gameplay_radius)
		if target:
			Orbwalker.Attacking = True
			ctx.attack(target)
			last_attacked = now
			
	if not target and dt > b_windup_time and now - last_moved > move_interval:	
		Orbwalker.Attacking = False
		
		# Check if mouse is within dead zone
		if ctx.w2s(player.pos).distance(ctx.cursor_pos) > dead_zone.radius and not player.channeling:
			ctx.move()
			last_moved = now
