from valkyrie import *

import os, json
from enum import Enum
from time import time
from .flags import Orbwalker, EvadeFlags

class ChannelSpell:
	def __init__(self, start_dist, end_dist, optimal_channel_time, max_channel_time, dist_calculator):
		'''
			@param start_dist, end_dist: the start distance at the start of the channel and at the end
			@param channel_time: the maximum time in seconds this spell can be channeled
			@param dist_calculator: must be a lambda with one float argument (the time since the beginning of the channel in seconds). it returns the distance that the spell will travel
		'''
		self.start_dist   = start_dist
		self.end_dist     = end_dist
		self.max_channel_time = max_channel_time
		self.optimal_channel_time = optimal_channel_time
		self.dist_calculator = dist_calculator
		
# Just some info about the chargeable spells in the game
ChargeableSpells = {
	'xeratharcanopulsechargeup': ChannelSpell(735.0, 1450.0, 0.0,  3.0, lambda t: min(1450.0, 735.0 + 408.0*t)),
	'varusq'                   : ChannelSpell(825.0, 1595.0, 1.25, 4.0, lambda t: min(1595.0, 825.0 + 560*t)),
	'pykeq'                    : ChannelSpell(400.0, 1100.0, 0.5,  3.0, lambda t: 400.0 if t <= 0.4 else min(1100.0, 400.0 + 1100*(t - 0.4))),
	'pantheonq'                : ChannelSpell(575.0, 1200.0, 0.4,  4.0, lambda t: 575 if t <= 0.4 else 1200.0),
	'sionq'                    : ChannelSpell(500.0, 850,    2.0,  2.0, lambda t: 500.0 if t <= 0.3 else min(850.0, 500.0 + 348*(t - 0.25))),
	'viq'                      : ChannelSpell(250.0, 715.0,  0.0,  4.0, lambda t: min(715.0, 250.0 + 372.0*t)),
	'vladimire'                : ChannelSpell(600.0, 600.0,  1.0,  1.5, lambda t: 600.0),
	'warwickq'                 : ChannelSpell(350.0, 350.0,  0.5,  0.5, lambda t: 350.0),
	'zace'                     : ChannelSpell(0.0,   1800.0, 1.3,  4.5, lambda t: min(1800.0, 1800*t/2.0)),
	'poppyr'                   : ChannelSpell(500.0, 1700.0, 0.5,  4.0, lambda t: 500.0 if t <= 0.5 else min(1700.0, 500 + 2400*(t - 0.5))),
	'ireliaw'                  : ChannelSpell(775.0, 775.0,  1.5,  1.5, lambda t: 775.0)
}

# Some spells cancel if orbwalker tries to move too fast
AfterCastPauses = {
	'xerathlocusofpower2' : 0.2
}

class CCType:
	Charm    = 0
	Stun     = 1
	Fear     = 2
	Slow     = 3
	Suppress = 4
	Root     = 5
	Taunt    = 6
	Drowsy   = 7
	Sleep    = 8
	Airbone  = 9
	
	Names = {
		Charm    : 'Charm',
		Stun     : 'Stun',     		
		Fear     : 'Fear',     		
		Slow     : 'Slow',     		
		Suppress : 'Suppress',
		Root     : 'Root',
		Taunt    : 'Taunt',
		Drowsy   : 'Drowsy',
		Sleep    : 'Sleep',
		Airbone  : 'Airbone'
	}

class BuffType:
	Mastery = 1
	CC      = 2
	Potion  = 4
	Poison  = 8

class Buff:
	
	def __init__(self, pretty_name, name, type, type_info = None):
		self.type = type
		self.type_info = type_info
		self.pretty_name = pretty_name
		self.name = name
		
	def is_type(self, type):
		return self.type & type == type

class Buffs:
	
	UnknownBuff = Buff('UnknownBuff', '?', 0)
	AllBuffs = [
		#    Pretty nam               In game name                 Type              More type info
		Buff('Charm',                'Charm',                      BuffType.CC,      CCType.Charm),
		Buff('Flee',                 'Flee',                       BuffType.CC,      CCType.Fear),
		Buff('Suppress',             'suppression',                BuffType.CC,      CCType.Suppress),
		Buff('Taunt',                'puncturingtauntattackspeed', BuffType.CC,      CCType.Taunt),

		# Stuns   
		Buff('Stun',                 'Stun',                       BuffType.CC,      CCType.Stun),
		Buff('VeigarEStun',          'veigareventhorizonstun',     BuffType.CC,      CCType.Stun),
		Buff('SonaRStun',            'SonaR',                      BuffType.CC,      CCType.Stun),

		# Airbones                                             
		Buff('RivenQKnockback',      'rivenknockback',             BuffType.CC,      CCType.Airbone),
		Buff('MalphiteRknockupstun', 'UnstoppableForceStun',       BuffType.CC,      CCType.Airbone),
		Buff('WukongRknockup',       'monkeykingspinknockup',      BuffType.CC,      CCType.Airbone),
		Buff('XinzhaoQknockup',      'XinZhaoQKnockup',            BuffType.CC,      CCType.Airbone),
		Buff('XinzhaoRknockback',    'xinzhaorknockback',          BuffType.CC,      CCType.Airbone),

		# Sleeps                                             
		Buff('ZoeEsleep',            'zoeesleepstun',              BuffType.CC,      CCType.Sleep),
								     
		# Slows                                              
		Buff('Slow',                 'slow',                       BuffType.CC,      CCType.Slow),
		Buff('WaterDrakeSlow',       'waterdragonslow',            BuffType.CC,      CCType.Slow),
		Buff('AshePassiveSlow',      'ashepassiveslow',            BuffType.CC,      CCType.Slow),
														      
		# Roots                                                    
		Buff('JhinWRoot',            'JhinW',                      BuffType.CC,      CCType.Root),
		Buff('LuxQRoot',             'LuxLightBindingMis',         BuffType.CC,      CCType.Root),
		Buff('RyzeWRoot',            'ryzewroot',                  BuffType.CC,      CCType.Root),
		Buff('SingedEWRoot',         'megaadhevisesnare',          BuffType.CC,      CCType.Root),
								 
		# Masteries                  
		Buff('LethalTempo',          'ASSETS/Perks/Styles/Precision/LethalTempo/LethalTempoEmpowered.lua', BuffType.Mastery),
		 
		# Potions
		Buff('DarkCrystalFlask',     'ItemDarkCrystalFlask',        BuffType.Potion),
		Buff('CrystalFlask',         'ItemCrystalFlask',            BuffType.Potion),
		Buff('RedPot',               'Item2003',                    BuffType.Potion),
		
		Buff('CassiopeiaQPoison',    'cassiopeiaqdebuff',           BuffType.Poison),
		Buff('CassiopeiaWPoison',    'cassiopeiawbuff',             BuffType.Poison),
	]
	
	AllBuffsDict = { buff.pretty_name : buff for buff in AllBuffs } | { buff.name : buff for buff in AllBuffs }

	@classmethod
	def has_buff(self, champ, buff_name):
		'''
			Check if champion has a buff.
		'''
		buff_obj = Buffs.AllBuffsDict.get(buff_name, None)
		if buff_obj == None:
			return False
			
		return champ.has_buff(buff_obj.name)
	
	@classmethod
	def has_buff_type(self, champ, buff_type):
		if type(champ) != ChampionObj:
			return False
			
		for buff in champ.buffs:
			b = Buffs.get(buff.name)
			if b.type == buff_type:
				return True
		return False
	
	@classmethod
	def has_cc_type(self, champ, cc_type):
		if type(champ) != ChampionObj:
			return False
			
		for buff in champ.buffs:
			b = Buffs.get(buff.name)
			if b.type != BuffType.CC:
				continue
			
			if b.type_info == cc_type:
				return True
				
		return False
	
	@classmethod
	def get(self, buff_name):
		'''
			Gets the buff object by name of the buff
		'''
		return Buffs.AllBuffsDict.get(buff_name, Buffs.UnknownBuff)

class Slot:
	''' 
		Spell slot indices. Usage: ChampionObj.spells[Slot.Q] 
	'''
	Q = 0
	W = 1
	E = 2
	R = 3
	D = 4
	F = 5
	
	SlotToStr = ['Q', 'W', 'E', 'R', 'D', 'F']
	
	@classmethod
	def to_str(self, slot):
		return self.SlotToStr[slot]

class SpellPredictor:
	def _ui(self, ctx, ui):
		pass
	
	def _predict(self, ctx, player, target, spell):
		return ctx.predict_cast_point(player, target, spell)

class RSpell:
	
	def __init__(self, slot, condition = None, predictor = SpellPredictor()):
		self.slot = slot
		self.condition = condition
		self.predictor = predictor
		
	def ui(self, ctx, ui):
		self.predictor._ui(ctx, ui)
		
		if self.condition:
			if ui.treenode('Trigger Condition'):
				ui.pushid(id(self.condition))
				self.condition.ui(ctx, ui)
				ui.separator()
				ui.popid()
				
				ui.treepop()
			ui.help('A trigger condition is logic that applies before casting the spell. For example a simple trigger would be "Target health trigger" that would check if the target HP is below a certain %, if the trigger is True then the spell is cast.')
		
	def check_condition(self, ctx, player, target, spell):
		if not self.condition:
			return True
			
		return self.condition.check(ctx, player, target, spell)
		
class SpellCondition:
	
	def __init__(self, enabled = True):
		self.enabled = enabled

	def check(self, ctx, player, target, spell):
		if self.enabled:
			return self._check(ctx, player, target, spell)
		return True

	def _check(self, ctx, player, target, spell):
		return True
		
	def _get_name(self):
		return 'Base Condition'
	
	def _get_help(self):
		return 'Condition help text'
	
	def ui(self, ctx, ui, depth = 0):
		
		self.enabled = ui.checkbox(self._get_name(), self.enabled)
		ui.help(self._get_help())
		if self.enabled:
			self._ui(ctx, ui)
		
	def _ui(self, ctx, ui):
		pass
		
class SpellRotation:
	'''
		Represents a rotation of spells
	'''

	IgnoreCurrentCast = set(['viq', 'zace', 'poppyr', 'ireliaw'])

	def __init__(self, rotation_spells, mask = None, charge_optimally = True):
		'''
			rotation_spells: must be an array of RSpell's
			mask: must be an array of booleans
		'''
		self.rotation_spells = rotation_spells
		if mask == None or len(rotation_spells) != len(mask):
			self.mask = [True for i in range(len(rotation_spells))]
		else:
			self.mask = mask
		
		self.chargeables = {}
		self.charge_optimally = charge_optimally
		self.pause_until = 0
		
	def find_spell(self, ctx, target_selector, target_extractor):
		'''
			Gets the next castable spell in the rotation. Returns None if nothing found
		'''
		player = ctx.player
		spells = player.spells
		
		for i, rspell in enumerate(self.rotation_spells):
			if not self.mask[i]:
				continue
				
			spell = spells[rspell.slot]
			if not spell.static or not player.can_cast_spell(spell):
				continue
				
			target = target_selector.get_target(ctx, target_extractor(ctx, player, spell))
			if not target:
				continue
				
			if not rspell.check_condition(ctx, player, target, spell):
				continue
				
			return target, spell, rspell
		
		return None, None, None
		
	def get_spell(self, ctx, player, target_selector, target_extractor):
		if player.curr_casting and player.curr_casting.remaining > 0.0:
			if player.curr_casting.name not in self.IgnoreCurrentCast:
				return None, None
			
		target, spell, rspell = self.find_spell(ctx, target_selector, target_extractor)
		if not spell:
			return None, None
		
		point = rspell.predictor._predict(ctx, player, target, spell)
		if not point:
			return None, None
		
		return spell, point
		
	def cast(self, ctx, target_selector, target_extractor):
		player = ctx.player
		now = time()
		if now < self.pause_until:
			return
			
		spell, point = self.get_spell(ctx, player, target_selector, target_extractor)
		if spell:
			if not spell.static.has_flag(Spell.ChannelSkill) and player.channeling:
				return
				
			if spell.static.has_flag(Spell.ChargeableSkill):
				chargeable_info = ChargeableSpells.get(spell.name, None)
				if not chargeable_info:
					return
					
				channel_start_time = self.chargeables.get(spell.name, None)
				if channel_start_time:
					dist_to_target = player.pos.distance(point) + 50.0
					dt = now - channel_start_time
					
					# Prevents bugs
					if dt < 0.2:
						return
						
					should_end = dt > chargeable_info.optimal_channel_time if self.charge_optimally else True
					if should_end and chargeable_info.dist_calculator(dt) > dist_to_target:
						ctx.end_channel(spell, point)
						self.chargeables[spell.name] = None
						
				elif ctx.start_channel(spell):
					self.chargeables[spell.name] = now
			else:
				if ctx.cast_spell(spell, point):
					pause = AfterCastPauses.get(spell.name, 0.0)
					if pause > 0.0:
						self.pause_until = now + pause
						Orbwalker.PauseUntil = now + pause
	
	def ui(self, ctx, ui):
		self.charge_optimally = ui.checkbox('Channel chargable spells until damage is maximized', self.charge_optimally)
		for i in range(len(self.mask)):
			slot = self.rotation_spells[i].slot
			slot_str = Slot.to_str(slot)
			
			spell = ctx.player.spells[slot]
			ui.image(spell.static.icon if spell.static else 'None', Vec2(16, 16), Col.White)
			ui.sameline()
			if ui.beginmenu(slot_str + ' ' + spell.name):
				self.mask[i] = ui.checkbox('Use spell', self.mask[i])
				self.rotation_spells[i].ui(ctx, ui)
				ui.endmenu()
