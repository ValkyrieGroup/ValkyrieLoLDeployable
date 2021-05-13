from valkyrie  import *
from .damages import calculate_onhit_dmg
import math

class MinionModifiers:

	LANE_TOP = 0
	LANE_MID = 1
	LANE_BOT = 2

	def __init__(self, ctx):


		# Calculate level advantages
		callies = ctx.champs.ally_to(ctx.player).get()
		cenemies = ctx.champs.enemy_to(ctx.player).get()

		ally_lvl = 0 if len(callies) == 0 else sum([c.lvl for c in callies])/len(callies)
		enemy_lvl = 0 if len(cenemies) == 0 else sum([c.lvl for c in cenemies])/len(cenemies)

		self.ally_level_advantage = min(3, max(0, ally_lvl - enemy_lvl))
		self.enemy_level_advantage = min(3, max(0, enemy_lvl - ally_lvl))

		# Calculate turret advantages
		tallies  = len(ctx.turrets.ally_to(ctx.player).alive().get())
		tenemies = len(ctx.turrets.enemy_to(ctx.player).alive().get())

        # Always assumes that turret advantage is 0, MUST FIX
		self.ally_turret_advantage  = 0.0
		self.enemy_turret_advantage = 0.0

		self.ally_dmg_modifier = 1.0 + (0.05 + (0.05 * self.ally_turret_advantage)) * self.ally_level_advantage
		self.enemy_dmg_modifier = 1.0 + (0.05 + (0.05 * self.enemy_turret_advantage)) * self.enemy_level_advantage
		self.ally_dmg_reduction = 1.0 + (self.ally_level_advantage * self.ally_turret_advantage)
		self.enemy_dmg_reduction = 1.0 + (self.enemy_level_advantage * self.enemy_turret_advantage)

def predict_minions_lasthit(ctx, enemy_minions, ally_minions, delay_percent = 0.0):
	'''
		Predicts the health of minions before the player basic attack hits, it returns a tuple (minion, new_health, hit_dmg) where:
			minion	 -> is the minion object
			new_health -> is the health of the minion after its been hit by the player
			hit_dmg	-> the hit dmg from the player
	'''

	player			 = ctx.player
	player_range	 = ctx.player.atk_range + ctx.player.static.gameplay_radius
	basic_atk_speed	 = player.static.basic_atk.speed if player.is_ranged else 20000.0
	basic_atk_delay	 = player.static.basic_atk_windup / player.atk_speed
	result = []

	modifiers = MinionModifiers(ctx)
	for enemy_minion in enemy_minions:

		hit_dmg		 		= calculate_onhit_dmg(ctx, player, enemy_minion)
		t_until_player_hits = basic_atk_delay + player.pos.distance(enemy_minion.pos) / basic_atk_speed
		enemy_minion_hp		= predict_minion_health(ctx, enemy_minion, ally_minions, t_until_player_hits, delay_percent, modifiers)
		
		if enemy_minion.pos.distance(player.pos) < player_range:
			result.append((enemy_minion, enemy_minion_hp, hit_dmg))
				
	return result

def predict_minion_health(ctx, enemy_minion, ally_minions, t_future, delay_percent, modifiers):
	'''
		Predicts the minion health of `enemy_minion` after `t_future` seconds elapse.
		It accomplishes this by checking the basic attacks of minions that are enemy to `enemy_minion`.
	'''
	enemy_minion_hp = math.ceil(enemy_minion.health)
	for ally_minion in ally_minions:
		
		casting = ally_minion.curr_casting
		if casting and casting.dest_index == enemy_minion.index and casting.static:
			t_until_ally_hits = (casting.cast_time - (ctx.time - casting.time_begin)) + ally_minion.pos.distance(enemy_minion.pos)/casting.static.speed

			dmg = math.floor(ally_minion.base_atk)
			if t_until_ally_hits > 0.0 and t_until_ally_hits < t_future:
				enemy_minion_hp -= (modifiers.enemy_dmg_reduction + dmg*modifiers.ally_dmg_modifier)
 
	return enemy_minion_hp