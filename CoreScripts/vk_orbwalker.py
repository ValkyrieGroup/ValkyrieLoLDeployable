from valkyrie import *
from helpers.targeting  import *
from helpers.prediction import *
from helpers.drawings   import Circle
from helpers.inputs     import KeyInput
from helpers.spells     import Buffs
from helpers.damages    import calculate_onhit_dmg
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

# Exceptions
extra_delay     = 0.0
atk_speed_override = None

not_attacks = [
	"asheqattacknoonhit",
	"volleyattackwithsound",
	"volleyattack",
	"annietibbersbasicattack",
	"annietibbersbasicattack2",
	"azirsoldierbasicattack",
	"azirsundiscbasicattack",
	"elisespiderlingbasicattack",
	"gravesbasicattackspread",
	"gravesautoattackrecoil",
	"heimertyellowbasicattack",
	"heimertyellowbasicattack2",
	"heimertbluebasicattack",
	"jarvanivcataclysmattack",
	"kindredwolfbasicattack",
	"malzaharvoidlingbasicattack",
	"malzaharvoidlingbasicattack2",
	"malzaharvoidlingbasicattack3",
	"shyvanadoubleattack",
	"shyvanadoubleattackdragon",
	"sivirwattackbounce",
	"monkeykingdoubleattack",
	"yorickspectralghoulbasicattack",
	"yorickdecayedghoulbasicattack",
	"yorickravenousghoulbasicattack",
	"zyragraspingplantattack",
	"zyragraspingplantattack2",
	"zyragraspingplantattackfire",
	"zyragraspingplantattack2fire"
]

class SpellTracker:
	spell_instance = None
	name = ""
	begin_time = 0
	remaining_time = 0

	auto_instance = None
	auto_begin = 0
	auto_windup_remaining = 0
	auto_last_attempt = 0
	auto_time_of_cancel = 0
	auto_attempt_interval = .5

	def update(self, ctx):
		current_casting = ctx.player.curr_casting

		if current_casting:
			spell_name = current_casting.name.lower()
			if "attack" not in spell_name and spell_name not in not_attacks:
				self.spell_instance = current_casting
				self.name = spell_name
				self.begin_time = current_casting.time_begin
				self.remaining_time = current_casting.remaining
			else:
				self.auto_instance = current_casting
				self.auto_windup_remaining = current_casting.remaining
				self.auto_begin = current_casting.time_begin
		else:
			self.spell_instance = None
			self.name = ""
			self.begin_time = 0
			self.remaining_time = 0

			if self.auto_instance:
				self.auto_time_of_cancel = ctx.time
			self.auto_instance = None

class OrbwalkKite:
	type = Orbwalker.ModeKite
	
	def get_target(self, ctx, distance):
		possible_targets = ctx.champs.targetable().enemy_to(ctx.player).near(ctx.player, distance).get()
		return target_selector.get_target(ctx, possible_targets)

class OrbwalkLastHit:
	type = Orbwalker.ModeKite

	def last_hit_score(self, minion: MinionObj, enemy_minions: list[MinionObj]):
		''' Returns a priority score for last hitting, first siege above all then the minion that is most attacked '''

		if 'siege' in minion.name:
			return 10000
		else:
			num_attackers = 0
			for m in enemy_minions:
				if m.curr_casting and m.curr_casting.dest_index == minion.index:
					num_attackers += 1

			return num_attackers

	def get_target(self, ctx, distance):
		lasthits = predict_minions_lasthit(ctx, ctx.minions.alive().enemy_to(ctx.player).on_screen().get(), ctx.minions.alive().ally_to(ctx.player).on_screen().get())
		if len(lasthits) == 0:
			return None

		# Find last hittable minions
		lasthits = sorted(lasthits, key = lambda p: p[0].health - p[1], reverse = True)
		last_hittable = []
		for minion, predicted_hp, player_dmg in lasthits:
			if predicted_hp - math.floor(player_dmg) <= 0.0:
				last_hittable.append(minion)

		if len(last_hittable) == 0:
			return None

		# Get best last hit
		ally_minions = ctx.minions.alive().ally_to(ctx.player).on_screen().get();
		return max(last_hittable, key = lambda m: self.last_hit_score(m, ally_minions))

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
			hit_dmg		 		= calculate_onhit_dmg(ctx, player, enemy_minion)
			
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
spell_tracker 	= SpellTracker()

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
	
	

def valkyrie_on_load(ctx: Context):
	global target_selector, max_atk_speed, move_interval, target_selector_monster, delay_percent
	global key_kite, key_last_hit, key_lane_push, dead_zone, extra_delay, atk_speed_override
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

	atk_speed_override = None
	if ctx.player.name == 'senna':
		extra_delay = 0.18
	if ctx.player.name == 'jhin':
		atk_speed_override = lambda player: 0.625 + 0.0177 * player.lvl
	
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


def valkyrie_exec(ctx: Context):
	Orbwalker.CurrentMode = None
	
	now = time()
	if now < Orbwalker.PauseUntil:
		return
		
	# Skip if player dead
	player = ctx.player   
	if player.dead:
		return
		
	dead_zone.draw_at(ctx, player.pos)
	spell_tracker.update(ctx)

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
	atk_speed        = 0.6

	if not atk_speed_override:
		atk_speed = player.atk_speed if has_lethal_tempo else min(player.atk_speed, 2.5)
	else:
		atk_speed = atk_speed_override(player)

	if atk_speed == 0.0:
		return
		
	c_atk_time	     = (1.0 + delay_percent)/atk_speed
	b_windup_time    = player.static.basic_atk_windup*c_atk_time						

	# moon gliding, animation canceling at perfect time
	for missile in ctx.missiles.near(ctx.player, 4000).get():
		mis_obj: MissileObj = missile

		if mis_obj.spell.src_index == player.index:
			mis_name = mis_obj.name.lower()
			if "attack" in mis_name and mis_name not in not_attacks:
				if ctx.time - mis_obj.first_seen > 0.15:
					b_windup_time = 0

	target = None
	dt = ctx.time - Orbwalker.LastAttacked - extra_delay
	can_auto = spell_tracker.remaining_time <= 0 and dt > c_atk_time

	auto_begin_t = ctx.time - spell_tracker.auto_begin
	auto_last_attempt_t = ctx.time - SpellTracker.auto_last_attempt
	auto_cancel_t = ctx.time - spell_tracker.auto_time_of_cancel

	# happens when you're casting a spell
	spell_reset = spell_tracker.spell_instance and spell_tracker.remaining_time <= 0 and \
				  auto_last_attempt_t > spell_tracker.auto_attempt_interval \
				  and c_atk_time > auto_begin_t and dt < b_windup_time + 0.25  # buffer for after cast check

	# happens when u manually click to move while winding up
	auto_canceled = not spell_tracker.auto_instance and auto_last_attempt_t > 0.05 and \
					(
						(auto_cancel_t > 0.05 and auto_begin_t < b_windup_time)
						# TODO: check for orb attack with no windup due to manual clicks
					)

	if not player.channeling and (can_auto or spell_reset or auto_canceled) and not Orbwalker.DisableAttack:
		target = Orbwalker.CurrentMode.get_target(ctx, player.atk_range + player.static.gameplay_radius)
		if target:
			Orbwalker.Attacking = True
			Orbwalker.LastAttacked = ctx.time
			ctx.attack(target)
			if spell_reset or auto_canceled:
				SpellTracker.auto_last_attempt = ctx.time
			return

	can_move = dt > b_windup_time
	if not target and can_move and ctx.time - Orbwalker.LastMoved > move_interval:
		Orbwalker.Attacking = False

		# Check if mouse is within dead zone
		if ctx.w2s(player.pos).distance(ctx.cursor_pos) > dead_zone.radius and not player.channeling:
			ctx.move()
			Orbwalker.LastMoved = ctx.time
