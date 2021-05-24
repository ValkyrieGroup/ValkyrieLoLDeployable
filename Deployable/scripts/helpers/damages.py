from valkyrie import *
import os, json

Calculations = {}

class Damage:

	def __init__(self, raw_dmg):
		self.raw_dmg = raw_dmg

	def calc_against(self, ctx, attacker, target):
		return 0.0

	def get_color(self, alpha = 1.0):
		col = self._color()
		return Col(col.r, col.g, col.b, alpha)

	def _color(self):
		return Col.Gray

class MagicDamage(Damage):
	def calc_against(self, ctx, attacker, target):
		return attacker.effective_magic_dmg(target, self.raw_dmg)

	def _color(self):
		return Col.Cyan

class PhysDamage(Damage):
	def calc_against(self, ctx, attacker, target):
		return attacker.effective_phys_dmg(target, self.raw_dmg)

	def _color(self):
		return Col.Orange

class TrueDamage(Damage):
	def calc_against(self, ctx, attacker, target):
		return self.raw_dmg

	def _color(self):
		return Col.White

class WrapMaxHP(Damage):
	def __init__(self, dmg_applied):
		self.dmg_applied = dmg_applied

	def calc_against(self, ctx, attacker, target):
		old_dmg = self.dmg_applied.raw_dmg

		self.dmg_applied.raw_dmg *= target.max_health
		result = self.dmg_applied.calc_against(ctx, attacker, target)

		self.dmg_applied.raw_dmg = old_dmg

		return result

	def _color(self):
		return self.dmg_applied._color()

class MixedDamage(Damage):

	def __init__(self, phys = None, magic = None, true = None, others=None):
		if others is None:
			others = []

		self.phys = phys
		self.magic = magic
		self.true = true
		self.others = others

	def calc_against(self, ctx, attacker, target):
		total = 0.0
		if self.phys:
			total += self.phys.calc_against(ctx, attacker, target)
		if self.magic:
			total += self.magic.calc_against(ctx, attacker, target)
		if self.true:
			total += self.true.calc_against(ctx, attacker, target)
		for dmg in self.others:
			total += dmg.calc_against(ctx, attacker, target)

		return total

	def add_individual(self, dmg1, dmg2, cls):
		if dmg1 == None:
			return cls(dmg2.raw_dmg) if dmg2 else None
		elif dmg2 == None:
			return cls(dmg1.raw_dmg) if dmg1 else None

		return cls(dmg1.raw_dmg + dmg2.raw_dmg)

	def __add__(self, other):
		dmg = MixedDamage(
			phys = self.phys,
			magic = self.magic,
			true = self.true,
			others = self.others
		)

		otype = type(other)
		if otype == MixedDamage:
			dmg.phys   = self.add_individual(self.phys, other.phys, PhysDamage)
			dmg.magic  = self.add_individual(self.magic, other.magic, MagicDamage)
			dmg.true   = self.add_individual(self.true, other.true, TrueDamage)
			dmg.others += other.others

		elif otype == PhysDamage:
			dmg.phys = self.add_individual(self.phys, other, PhysDamage)
		elif otype == MagicDamage:
			dmg.magic = self.add_individual(self.magic, other, MagicDamage)
		elif otype == TrueDamage:
			dmg.true = self.add_individual(self.true, other, TrueDamage)
		else:
			dmg.others.append(other)

		return dmg

	def _color(self):
		return Col.Red

class TwitchExpungeDamage(MixedDamage):
	def __init__(self, base, phys, magic):
		self.base = base
		self.phys = phys
		self.magic = magic

	def calc_against(self, ctx, attacker, target):
		stacks = 0
		if target.has_buff('TwitchDeadlyVenom'):
			stacks = target.get_buff('TwitchDeadlyVenom').value

		return self.base.calc_against(ctx, attacker, target) + stacks*self.phys.calc_against(ctx, attacker, target) + stacks*self.magic.calc_against(ctx, attacker, target)

class KalistaExpungeWrapperDamage(PhysDamage):
	def __init__(self, base, phys):
		self.base = base
		self.phys = phys

	def calc_against(self, ctx, attacker, target):
		stacks = target.num_buff_stacks('kalistaexpungemarker')

		return self.base.calc_against(ctx, attacker, target) + stacks*self.phys.calc_against(ctx, attacker, target)

class CassiopeiaEDamage(MagicDamage):
	def __init__(self, base, bonus):
		self.base = base
		self.bonus = bonus

	def calc_against(self, ctx, attacker, target):

		dmg = self.base.calc_against(ctx, attacker, target)

		if type(target) == ChampionObj:
			poisoned = target.has_buff('cassiopeiaqdebuff') or target.has_buff('cassiopeiawbuff')
			if poisoned:
				dmg += self.bonus.calc_against(ctx, attacker, target)

		return dmg

class KogMawRDamage(MagicDamage):

	def calc_against(self, ctx, attacker, target):
		p = target.health/target.max_health
		if p < 0.4:
			self.raw_dmg *= 2.0
			dmg = super().calc_against(ctx, attacker, target)
			self.raw_dmg /= 2.0
		else:
			dmg = super().calc_against(ctx, attacker, target)

		return dmg

class DariusRDamage(TrueDamage):

	def __init__(self, base):
		self.base = base

	def calc_against(self, ctx, attacker, target):
		num_stacks = target.num_buff_stacks('DariusHemo')
		return self.base + self.base * (0.2*num_stacks)

class SyndraRDamage(MagicDamage):

	def __init__(self, base):
		self.base = base

	def calc_against(self, ctx, attacker, target):
		self.raw_dmg = self.base * min(7, 3 + len(ctx.others.has_tag(Unit.SpecialSyndraSphere).alive().get()))

		return super().calc_against(ctx, attacker, target)


class TristanaEDamage(MagicDamage):
	def __init__(self, base, bonus_per_stack):
		self.base = base
		self.bonus_per_stack = bonus_per_stack

	def calc_against(self, ctx, attacker, target):
		self.raw_dmg = self.base + self.base * 1.2
		self.raw_dmg = self.raw_dmg + self.raw_dmg * (0.033*attacker.crit/0.1)

		return super().calc_against(ctx, attacker, target)

class DianaRDamage(MagicDamage):
	def __init__(self, base, bonus_per_champ):
		self.base = base
		self.bonus_per_champ = bonus_per_champ

	def calc_against(self, ctx, attacker, target):
		num_champs = len(ctx.champs.enemy_to(attacker).targetable().near(attacker, 475).get())
		self.raw_dmg = self.base + num_champs * self.bonus_per_champ
		return super().calc_against(ctx, attacker, target)

class JinxRDmage(PhysDamage):

	missing_hp = [0.25, 0.30, 0.35]
	def __init__(self, base):
		self.base = base

	def calc_against(self, ctx, attacker, target):

		lvl = max(0, attacker.spells[3].lvl - 1)
		mhp = self.missing_hp[lvl]
		multi = min(1.0, 0.1 + 0.06 * attacker.pos.distance(target.pos) / 100.0)

		self.raw_dmg = self.base*multi + mhp*(target.max_health - target.health)
		return super().calc_against(ctx, attacker, target)

class VeigarRDamage(MagicDamage):

	def __init__(self, base):
		self.base = base

	def calc_against(self, ctx, attacker, target):
		p = target.health/target.max_health
		self.raw_dmg = self.base + self.base * min(0.66, (1.0 - p)*1.5)
		return super().calc_against(ctx, attacker, target)

class XerathRDamage(MagicDamage):

	def __init__(self, base):
		self.base = base

	def calc_against(self, ctx, attacker, target):
		stacks = 0
		buff = attacker.get_buff('xerathrshots')
		if not buff:
			stacks = 2 + attacker.spells[3].lvl
		else:
			stacks = buff.value

		self.raw_dmg = stacks*self.base
		return super().calc_against(ctx, attacker, target)

class DivineSundererDamage(PhysDamage):

	def __init__(self):
		self.raw_dmg = 0.0

	def calc_against(self, ctx, attacker, target):
		self.raw_dmg = max(attacker.base_atk * 1.5, target.max_health * 0.1)
		return super().calc_against(ctx, attacker, target)

class BotrkDamage(PhysDamage):

	def __init__(self):
		self.raw_dmg = 0.0

	def calc_against(self, ctx, attacker, target):
		dmg = target.health * (0.06 if attacker.is_ranged else 0.1)
		if dmg > 60.0 and not target.has_tags(Unit.Champion):
			self.raw_dmg = 60.0
		else:
			self.raw_dmg = dmg

		return super().calc_against(ctx, attacker, target)

class NoonquiverDamage(PhysDamage):

	def __init__(self):
		self.raw_dmg = 0.0

	def calc_against(self, ctx, attacker, target):
		self.raw_dmg = 0.0 if target.has_tags(Unit.Champion) else 20.0

		return super().calc_against(ctx, attacker, target)

DamageExtractors = {

	# Ahri
	'ahriorbofdeception'     : lambda calc, champ, skill: MixedDamage(magic = MagicDamage(calc.totaldamage(champ, skill)), true = TrueDamage(calc.totaldamage(champ, skill))),
	'ahrifoxfire'            : lambda calc, champ, skill: MagicDamage(calc.singlefiredamage(champ, skill) + calc.multifiredamage(champ, skill)*2.0),
	'ahriseduce'             : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'ahritumble'             : lambda calc, champ, skill: MagicDamage(calc.rcalculateddamage(champ, skill) * 3.0),

	# Ashe
	'volley'                 : lambda calc, champ, skill: PhysDamage(calc.totaldamage(champ, skill)),
    'volleyrank2'            : lambda calc, champ, skill: PhysDamage(calc.totaldamage(champ, skill)),
    'volleyrank3'            : lambda calc, champ, skill: PhysDamage(calc.totaldamage(champ, skill)),
    'volleyrank4'            : lambda calc, champ, skill: PhysDamage(calc.totaldamage(champ, skill)),
    'volleyrank5'            : lambda calc, champ, skill: PhysDamage(calc.totaldamage(champ, skill)),
	'enchantedcrystalarrow'  : lambda calc, champ, skill: MagicDamage(calc.rmaindamage(champ, skill)),

	# Annie
	'annieq'                 : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'anniew'                 : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'annier'                 : lambda calc, champ, skill: MagicDamage(calc.initialburstdamage(champ, skill)),

    # Chogath
	'feast'                  : lambda calc, champ, skill: TrueDamage(calc.rdamage(champ, skill)),

	# Darius
	'dariuscleave'           : lambda calc, champ, skill: PhysDamage(calc.bladedamage(champ, skill)),
	'dariusnoxiantacticsonh' : lambda calc, champ, skill: PhysDamage(calc.empoweredattackdamage(champ, skill)),
	'dariusexecute'          : lambda calc, champ, skill: DariusRDamage(calc.damage(champ, skill)),

	# Diana
	'dianaq'                 : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'dianaorbs'              : lambda calc, champ, skill: MagicDamage(calc.totalmaxdamage(champ, skill)),
	'dianateleport'          : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'dianar'                 : lambda calc, champ, skill: DianaRDamage(calc.rexplosiondamage(champ, skill), calc.rmultihitamplification(champ, skill)),

        # Draven
	'dravenrcast'            : lambda calc, champ, skill: PhysDamage(calc.rcalculateddamage(champ, skill)),

	# Ezreal
	'ezrealq'                : lambda calc, champ, skill: PhysDamage(calc.damage(champ, skill)),
	'ezrealw'                : lambda calc, champ, skill: MagicDamage(calc.damage(champ, skill)),
	'ezreale'                : lambda calc, champ, skill: MagicDamage(calc.damage(champ, skill)),
	'ezrealr'                : lambda calc, champ, skill: MagicDamage(calc.damage(champ, skill)),

	# Fiora
	'fioraq'                 : lambda calc, champ, skill: PhysDamage(calc.totaldamage(champ, skill)),
	'fioraw'                 : lambda calc, champ, skill: MagicDamage(calc.stabdamage(champ, skill)),
	'fiorar'                 : lambda calc, champ, skill: WrapMaxHP(TrueDamage(4.0 * Calculations['fiorapassive'].passivedamagetotal(champ, skill))),

	# Hecarim
	'hecarimrapidslash'      : lambda calc, champ, skill: PhysDamage(calc.damage(champ, skill)),
	'hecarimw'               : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'hecarimramp'            : lambda calc, champ, skill: PhysDamage(calc.mindamage(champ, skill)),
	'hecarimult'             : lambda calc, champ, skill: MagicDamage(calc.damagedone(champ, skill)),

        # Kalista
	'kalistaexpungewrapper'  : lambda calc, champ, skill: KalistaExpungeWrapperDamage(PhysDamage(calc.basedamage[skill.lvl - 1]), PhysDamage(calc.additionaldamage(champ, skill))),

	# Irelia
	'ireliaq'                : lambda calc, champ, skill: PhysDamage(calc.championdamage(champ, skill)),
	'ireliaw'                : lambda calc, champ, skill: PhysDamage(calc.maxdamagecalc(champ, skill)),
	'ireliae'                : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'ireliar'                : lambda calc, champ, skill: MagicDamage(calc.missiledamage(champ, skill)),

	# Jinx
	'jinxw'                  : lambda calc, champ, skill: PhysDamage(calc.totaldamage(champ, skill)),
	'jinxe'                  : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'jinxr'                  : lambda calc, champ, skill: JinxRDmage(calc.damagemax(champ, skill)),
	
    # Katarina
    'katarinapassive'        : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
    'katarinaq'              : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
    'katarinaewrapper'       : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
    'katarinar'              : lambda calc, champ, skill: MixedDamage(phys = PhysDamage(calc.totaladdamagecalc(champ, skill)), magic = MagicDamage(calc.totaldamagecalc(champ, skill))),
	
	# Kayle
	'kayleq'                 : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'kayler'                 : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),

	# Cassiopeia
	'cassiopeiaq'            : lambda calc, champ, skill: MagicDamage(calc.tooltiptotaldamage(champ, skill)),
	'cassiopeiaw'            : lambda calc, champ, skill: MagicDamage(calc.damagepersecond(champ, skill)*5.0),
	'cassiopeiae'            : lambda calc, champ, skill: CassiopeiaEDamage(MagicDamage(calc.totaldamage(champ, skill)), MagicDamage(calc.bouspoisoneddamage(champ, skill))),
	'cassiopeiar'            : lambda calc, champ, skill: MagicDamage(calc.rdamage(champ, skill)),

	# Kogmaw
	'kogmawq'                : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'kogmawvoidooze'         : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'kogmawlivingartillery'  : lambda calc, champ, skill: KogMawRDamage(calc.basedamagecalc(champ, skill)),

	# Olaf
	'olafaxethrowcast'       : lambda calc, champ, skill: PhysDamage(calc.totaldamage(champ, skill)),
	'olafrecklessstrike'     : lambda calc, champ, skill: TrueDamage(calc.totaldamage(champ, skill)),

        # Pyke
	'pyker'                  : lambda calc, champ, skill: PhysDamage(calc.rdamage(champ, skill)),

	# Samira
	'samiraq'                : lambda calc, champ, skill: PhysDamage(calc.damagecalc(champ, skill)),
	'samiraw'                : lambda calc, champ, skill: PhysDamage(calc.damagecalc(champ, skill)),
	'samirae'                : lambda calc, champ, skill: MagicDamage(calc.dashdamage(champ, skill)),
	'samirar'                : lambda calc, champ, skill: PhysDamage(11.0 * calc.damagecalc(champ, skill)),

	# Senna
	'sennaq'                 : lambda calc, champ, skill: PhysDamage(calc.totaldamage(champ, skill)),
    'sennaw'                 : lambda calc, champ, skill: PhysDamage(calc.damage(champ, skill)),
    'sennar'                 : lambda calc, champ, skill: PhysDamage(calc.totaldamage(champ, skill)),

	# Soraka
	'sorakaq'                : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'sorakae'                : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)*2.0),

	# Syndra
	'syndraq'                : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'syndraw'                : lambda calc, champ, skill: MagicDamage(calc.throwdamage(champ, skill)),
	'syndrae'                : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'syndrar'                : lambda calc, champ, skill: SyndraRDamage(calc.damagecalc(champ, skill)),

	# Teemo
	'blindingdart'           : lambda calc, champ, skill: MagicDamage(calc.calculateddamage(champ, skill)),
	'teemorcast'             : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),

	# Tristana
	'tristanaw'              : lambda calc, champ, skill: MagicDamage(calc.landingdamage(champ, skill)),
	'tristanae'              : lambda calc, champ, skill: TristanaEDamage(calc.activedamage(champ, skill), calc.activemaxdamage(champ, skill)),
	'tristanar'              : lambda calc, champ, skill: MagicDamage(calc.damagecalc(champ, skill)),

	# Twitch
	'twitchexpunge'          : lambda calc, champ, skill: TwitchExpungeDamage(PhysDamage(calc.basedamage[skill.lvl - 1]), PhysDamage(calc.physicaldamageperstack(champ, skill)), MagicDamage(calc.magicdamageperstack(champ, skill))),

	# Urgot
	'urgotq'                 : lambda calc, champ, skill: PhysDamage(calc.totaldamage(champ, skill)),
	'urgotw'                 : lambda calc, champ, skill: PhysDamage(12.0 * calc.damagepershot(champ, skill)),
	'urgote'                 : lambda calc, champ, skill: PhysDamage(calc.edamage(champ, skill)),
	'urgotr'                 : lambda calc, champ, skill: PhysDamage(calc.rcalculateddamage(champ, skill)),

	# Vayne
	'vaynetumble'            : lambda calc, champ, skill: PhysDamage(calc.adratiobonus(champ, skill)),
	'vaynesilveredbolts'     : lambda calc, champ, skill: WrapMaxHP(TrueDamage(calc.maxhealthratio[skill.lvl - 1])),
	'vaynecondemn'           : lambda calc, champ, skill: PhysDamage(calc.totaldamage(champ, skill)),

	# Veigar
	'veigarbalefulstrike'    : lambda calc, champ, skill: MagicDamage(calc.totaldamagetooltip(champ, skill)),
	'veigardarkmatter'       : lambda calc, champ, skill: MagicDamage(calc.totaldamagetooltip(champ, skill)),
	'veigarr'                : lambda calc, champ, skill: VeigarRDamage(calc.mindamagetooltip(champ, skill)),

        # Viktor
	'viktorpowertransfer'    : lambda calc, champ, skill: MagicDamage(calc.totalmissiledamage(champ, skill)),
	'viktordeathray'         : lambda calc, champ, skill: MagicDamage(calc.laserdamage(champ, skill)),
	'viktorchaosstorm'       : lambda calc, champ, skill: MagicDamage(calc.initialburstdamage(champ, skill)),

	# Vladimir
	'vladimirq'              : lambda calc, champ, skill: MagicDamage(calc.basedamagetooltip(champ, skill)),
	'vladimirhemoplague'     : lambda calc, champ, skill: MagicDamage(calc.damage(champ, skill)),

	# Yasuo
	'yasuoq1wrapper'         : lambda calc, champ, skill: PhysDamage(calc.totaldamagecrit(champ, skill)),
	'yasuoq2wrapper'         : lambda calc, champ, skill: PhysDamage(calc.totaldamagecrit(champ, skill)),
	'yasuoq3wrapper'         : lambda calc, champ, skill: PhysDamage(calc.totaldamagecrit(champ, skill)),
	'yasuoe'                 : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'yasuor'                 : lambda calc, champ, skill: PhysDamage(calc.damage(champ, skill)),

    # Yone
	'yoneq'                  : lambda calc, champ, skill: PhysDamage(calc.totaldamagecrit(champ, skill)),
	'yoneq3'                 : lambda calc, champ, skill: PhysDamage(calc.totaldamagecrit(champ, skill)),
	'yonew'                  : lambda calc, champ, skill: PhysDamage(calc.wdamage(champ, skill)),
	'yoner'                  : lambda calc, champ, skill: PhysDamage(calc.damage(champ, skill)),

	# Xerath
	'xeratharcanopulsechargeup' : lambda calc, champ, skill: MagicDamage(calc.tooltiptotaldamage(champ, skill)),
	'xeratharcanebarrage2'      : lambda calc, champ, skill: MagicDamage(calc.totaldamage(champ, skill)),
	'xerathmagespear'           : lambda calc, champ, skill: MagicDamage(calc.tooltiptotaldamage(champ, skill)),
	'xerathlocusofpower2'       : lambda calc, champ, skill: XerathRDamage(calc.tooltiptotaldamage(champ, skill)),
	'xerathrmissilewrapper'     : lambda calc, champ, skill: XerathRDamage(calc.tooltiptotaldamage(champ, skill))
}

DuplicateMap = {
	'yasuoq1wrapper': ['yasuoq2wrapper', 'yasuoq3wrapper'],
	'xerathlocusofpower2': ['xerathrmissilewrapper']
}

def load_spell_calcs(path):
	global Calculations

	j = {}
	with open(path, 'r') as f:
		j = json.loads(f.read())


	for name, vdict in j.items():
		lname = name.lower()
		if lname in Calculations:
			continue

		obj_dict = {}
		for dval_name, dval_values in vdict['data_vals'].items():
			obj_dict[dval_name] = dval_values

		for formula_name, formula_str in vdict['calcs'].items():
			if '{' not in formula_str and '{' not in formula_name:
				exec(f'def {formula_name}(self, champ, skill): return {formula_str}')
				obj_dict[formula_name] = eval(formula_name)

		obj = type('spell_' + lname, (object, ), obj_dict)()
		Calculations[lname] = obj
		dupes = DuplicateMap.get(lname, [])
		for name in dupes:
			Calculations[name] = obj

class OnHitCalculator:
	def calculate(self, source, target) -> (int, int):
		return get_items_onhit_damage(source) + PhysDamage(source.base_atk + source.bonus_atk)

class KalistaOnHitCalculator(OnHitCalculator):
	def calculate(self, source, target) -> (int, int):
		dmg = super().calculate(source, target)
		dmg.phys.raw_dmg *= 0.9
		return dmg

class QuinnOnHitCalculator(OnHitCalculator):
	def calculate(self, source, target) -> (int, int):
		dmg = super().calculate(source, target)

		if target.has_buff('QuinnW'):
			calcs = Calculations.get('quinnpassive', None)
			dmg.phys.raw_dmg += calcs.bonusdamage(source, None)

		return dmg

class OriannaOnHitCalculator(OnHitCalculator):
	def calculate(self, source, target) -> (int, int):
		dmg = super().calculate(source, target)

		calcs = Calculations.get('oriannap', None)
		dmg.magic.raw_dmg += calcs.totaldamage(source, None)

		return dmg

class OnHitInfo:

	def __init__(self, damage_solver = lambda src, spell: PhysDamage(0.0), only_basics=False):
		self.damage_solver = damage_solver
		self.only_basics = only_basics

	def get_damage(self, slot, source, spell):
		if spell:
			if self.only_basics or not spell.static.has_flag(Spell.AppliesOnHit):
				return PhysDamage(0.0)

			if not slot.active or slot.active.cd > 0.0:
				return PhysDamage(0.0)

			return self.damage_solver(source, spell)

		return self.damage_solver(source, None)

def crit_from_items(item_slots):
	crit = 0.0
	for slot in item_slots:
		if slot.item:
			crit += slot.item.crit
	return crit


def onhit_guinsoo(src, spell):
	return PhysDamage(min(200.0, min(crit_from_items(src.item_slots), 1.0) * 100.0 * 2.0))


def onhit_rageknife(src, spell):
	return PhysDamage(min(175.0, min(crit_from_items(src.item_slots), 1.0) * 100.0 * 1.75))


def onhit_noonquiver(src, spell):
	return NoonquiverDamage()


def onhit_recurve_bow(src, spell):
	return PhysDamage(15.0)


def onhit_botrk(src, spell):
	return BotrkDamage()

def onhit_doran_ring(src, spell):
	return PhysDamage(5.0)


def onhit_nashors(src, spell):
	return MagicDamage(15.0 + 0.2 * src.ap)


def onhit_wits_end(src, spell):
	return MagicDamage(15.0 + 3.82 * (src.lvl - 1))


def onhit_titanic_hydra(src, spell):
	dmg = 3.75 if src.is_ranged else 5
	dmg += (src.max_health * 0.01125 if src.is_ranged else 0.015)

	return PhysDamage(dmg)


def onhit_sheen(src, spell):
	if spell or src.has_buff('sheen'):
		return PhysDamage(src.base_atk)
	return PhysDamage(0.0)


def onhit_trinity(src, spell):
	if spell or src.has_buff('3078trinityforce'):
		return PhysDamage(2.0 * src.base_atk)
	return PhysDamage(0.0)


def onhit_kraken(src, spell):
	buff = src.get_buff('6672buff')
	if buff and buff.value == 2:
		return TrueDamage(60.0 + 0.45 * src.bonus_atk)
	return PhysDamage(0.0)


def onhit_divine_sunderer(src, spell):
	if spell or src.has_buff('6632buff'):
		return DivineSundererDamage()
	return PhysDamage(0.0)

def onhit_lichbane(src, spell):
	if spell or src.has_buff('lichbane'):
		return MagicDamage(1.5 * src.base_atk + 0.4 * src.ap)
	return MagicDamage(0.0)

def onhit_essence_reaver(src, spell):
	if spell or src.has_buff('3508buff'):
		return PhysDamage(src.base_atk + 0.4*src.bonus_atk)
	return PhysDamage(0.0)

OnHits = {
	3124: OnHitInfo(damage_solver=onhit_guinsoo),
	6677: OnHitInfo(damage_solver=onhit_rageknife),
	6670: OnHitInfo(damage_solver=onhit_noonquiver, only_basics=True),
	1043: OnHitInfo(damage_solver=onhit_recurve_bow),
	3153: OnHitInfo(damage_solver=onhit_botrk),
	1056: OnHitInfo(damage_solver=onhit_doran_ring, only_basics=True),
	3748: OnHitInfo(damage_solver=onhit_titanic_hydra),

	3115: OnHitInfo(damage_solver=onhit_nashors),
	3091: OnHitInfo(damage_solver=onhit_wits_end),
	3100: OnHitInfo(damage_solver=onhit_lichbane),
	3508: OnHitInfo(damage_solver=onhit_essence_reaver),
	6672: OnHitInfo(damage_solver=onhit_kraken),
	6632: OnHitInfo(damage_solver=onhit_divine_sunderer),
	3057: OnHitInfo(damage_solver=onhit_sheen),
	3078: OnHitInfo(damage_solver=onhit_trinity)
}

DefaultOnHitCalculator = OnHitCalculator()
ChampionOnHitCalculators = {
	'kalista' : KalistaOnHitCalculator(),
	'quinn'   : QuinnOnHitCalculator(),
	'orianna' : OriannaOnHitCalculator()
}

def get_items_onhit_damage(source, spell=None) -> MixedDamage:
	''' Returns raw on hit damage from items as atuple (physical_damage, magical_damage) '''

	dmg = MixedDamage()
	for slot in source.item_slots:
		item = slot.item
		if not item:
			continue

		calculator = OnHits.get(item.id, None)
		if not calculator:
			continue

		dmg = dmg + calculator.get_damage(slot, source, spell)

	return dmg

def calculate_onhit_dmg(ctx: Context, source: UnitObj, target: UnitObj) -> float:
	return ChampionOnHitCalculators.get(source.name, DefaultOnHitCalculator).calculate(source, target).calc_against(ctx, source, target)

def calculate_raw_spell_dmg(champ: ChampionObj, spell: SpellObj) -> Damage:
	calculations = Calculations.get(spell.name, None)
	if calculations == None:
		return Damage(0.0)

	extractor = DamageExtractors.get(spell.name, None)
	if extractor == None:
		return Damage(0.0)

	dmg = extractor(calculations, champ, spell)
	if spell.static.has_flag(Spell.AppliesOnHit):
		return get_items_onhit_damage(champ, spell) + dmg

	return dmg


load_spell_calcs(os.path.join(os.getenv('APPDATA'), 'Valkyrie\data\SpellCalculations.json'))
