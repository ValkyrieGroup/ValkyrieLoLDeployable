from valkyrie import *
from helpers.damages import calculate_raw_spell_dmg

BasePosition : Vec3

class BaseUltor:

	def __init__(self, ranges, travel_time_solver, cast_time, raycast = False):
		self.ranges = ranges
		self.travel_time_solver = travel_time_solver
		self.cast_time = cast_time
		self.raycast = raycast

	def check(self, ctx: Context, player: ChampionObj, target: ChampionObj, time_until_recalls: float):
		distance = player.pos.distance(BasePosition)
		if distance > self.ranges[player.R.lvl - 1]:
			return False

		travel_time = self.cast_time + self.travel_time_solver(distance)
		time_diff = travel_time - time_until_recalls
		if time_diff > 0.0 and time_diff < 0.1:
			if self.raycast:
				ray = ctx.raycast(player.pos, (BasePosition - player.pos).normalize(), distance, 100.0, (RayLayer)(RayLayer.Enemy | RayLayer.Champion))
				if ray and ray.obj.visible:
					return False
			return True
		return False

def jinx_travel_time_solver(dist):
	if dist < 1350.0:
		return dist/1700.0

	travel_time = 1350.0/1700.0
	travel_time += (dist - 1350.0)/2200.0

	return travel_time

OnlyIfInFog : bool
CurrentUltor: BaseUltor

Ultors = {
	'ezreal'     : BaseUltor(ranges = [25000.0, 25000.0, 25000.0], travel_time_solver = lambda dist: dist/2000.0,  cast_time = 1.0),
	'jinx'       : BaseUltor(ranges = [25000.0, 25000.0, 25000.0], travel_time_solver = jinx_travel_time_solver,   cast_time = 0.6, raycast = True),
    'ashe'       : BaseUltor(ranges = [25000.0, 25000.0, 25000.0], travel_time_solver = lambda dist: dist/1600.0,  cast_time = 0.25, raycast = True),
	'draven'     : BaseUltor(ranges = [25000.0, 25000.0, 25000.0], travel_time_solver = lambda dist: dist/2000.0,  cast_time = 0.5),
	'senna'      : BaseUltor(ranges = [25000.0, 25000.0, 25000.0], travel_time_solver = lambda dist: dist/20000.0, cast_time = 1.0)
}

def valkyrie_menu(ctx: Context):
	global OnlyIfInFog
	ui = ctx.ui

	if CurrentUltor:
		ui.text_color('This champion has base ult support', Col.Green)
	else:
		ui.text_color('Champion is not supported by base ult', Col.Red)
		return

	ui.separator()
	OnlyIfInFog             = ui.checkbox('Ult ONLY if champion is in fog of war', OnlyIfInFog)


def valkyrie_on_load(ctx: Context):
	global CurrentUltor, BasePosition
	global OnlyIfInFog

	cfg = ctx.cfg
	CurrentUltor = Ultors.get(ctx.player.name, None)
	if ctx.player.team == 200:
		BasePosition = Vec3(394.0, 182.13, 462.0)
	else:
		BasePosition = Vec3(14320.0, 171.0, 14414.0)

	OnlyIfInFog             = cfg.get_bool('OnlyIfInFog', False)

def valkyrie_on_save(ctx: Context):
	cfg = ctx.cfg

	cfg.set_bool('OnlyIfInFog', OnlyIfInFog)

def valkyrie_exec(ctx: Context):

	player = ctx.player

	if not CurrentUltor or player.dead or not player.can_cast_spell(player.R):
		return

	dmg = calculate_raw_spell_dmg(player, player.R)
	champs = ctx.champs.enemy_to(player).invisible().get() if OnlyIfInFog else ctx.champs.enemy_to(player).get()
	for champ in champs:
		if champ.recalling:
			# Check enough damage
			if dmg.calc_against(ctx, player, champ) < champ.health:
				continue

			recalling_for  = ctx.time - champ.recall_start_time
			recall_duration = 4.0 if champ.has_buff('exaltedwithbaronnashor') else 8.0
			left_recalling = recall_duration - recalling_for

			if CurrentUltor.check(ctx, player, champ, left_recalling):
				ctx.cast_spell(player.R, BasePosition)
