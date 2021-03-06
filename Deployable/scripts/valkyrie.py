### ---> THIS IS AN AUTOMATICALLY GENERATED FILE. IT IS USED FOR AUTOCOMPLETION IN YOUR FAVORITE IDE <--- ###
from __future__ import annotations

class Config:
	'''Interface for saving & loading script configurations'''

	def set_int(self, key: str, value: int):
		'''    Saves an integer to the config file'''
		pass

	def set_bool(self, key: str, value: bool):
		'''    Saves a bool to the config file'''
		pass

	def set_float(self, key: str, value: float):
		'''    Saves a float to the config file'''
		pass

	def set_str(self, key: str, value: str):
		'''    Saves a string to the config file'''
		pass

	def get_int(self, key: str, default: int) -> int:
		'''    Gets an integer from the config file'''
		pass

	def get_bool(self, key: str, default: bool) -> bool:
		'''    Gets a bool from the config file'''
		pass

	def get_float(self, key: str, default: float) -> float:
		'''    Gets a float from the config file'''
		pass

	def get_str(self, key: str, default: str) -> str:
		'''    Gets a string from the config file'''
		pass

class Col:
	'''None'''

	Black : any
	White : any
	Red : any
	DarkRed : any
	Green : any
	DarkGreen : any
	Yellow : any
	DarkYellow : any
	Cyan : any
	Purple : any
	Gray : any
	Orange : any
	Blue : any
	Brown : any
	@property
	def r(self) -> float:
		''' Red value of color'''
		pass

	@r.setter
	def r(self, value):
		''' Red value of color'''
		pass

	@property
	def g(self) -> float:
		''' Green value of color'''
		pass

	@g.setter
	def g(self, value):
		''' Green value of color'''
		pass

	@property
	def b(self) -> float:
		''' Blue value of color'''
		pass

	@b.setter
	def b(self, value):
		''' Blue value of color'''
		pass

	@property
	def a(self) -> float:
		''' Alpha value of color'''
		pass

	@a.setter
	def a(self, value):
		''' Alpha value of color'''
		pass

class Vec4:
	'''None'''

	@property
	def x(self) -> float:
		''''''
		pass

	@x.setter
	def x(self, value):
		''''''
		pass

	@property
	def y(self) -> float:
		''''''
		pass

	@y.setter
	def y(self, value):
		''''''
		pass

	@property
	def z(self) -> float:
		''''''
		pass

	@z.setter
	def z(self, value):
		''''''
		pass

	@property
	def w(self) -> float:
		''''''
		pass

	@w.setter
	def w(self, value):
		''''''
		pass

	def length(self) -> float:
		'''    '''
		pass

	def normalize(self) -> float:
		'''    '''
		pass

	def distance(self, other: Vec4) -> float:
		'''    '''
		pass

	def clone(self) -> Vec4:
		'''    '''
		pass

class Vec3:
	'''None'''

	@property
	def x(self) -> float:
		''''''
		pass

	@x.setter
	def x(self, value):
		''''''
		pass

	@property
	def y(self) -> float:
		''''''
		pass

	@y.setter
	def y(self, value):
		''''''
		pass

	@property
	def z(self) -> float:
		''''''
		pass

	@z.setter
	def z(self, value):
		''''''
		pass

	def length(self) -> float:
		'''    '''
		pass

	def normalize(self) -> float:
		'''    '''
		pass

	def distance(self, other: Vec3) -> float:
		'''    '''
		pass

	def l1(self, other: Vec3) -> float:
		'''    L1 Distance'''
		pass

	def rotate_x(self, angle: float) -> Vec3:
		'''    Rotates the vector along the x axis'''
		pass

	def rotate_y(self, angle: float) -> Vec3:
		'''    Rotates the vector along the y axis'''
		pass

	def rotate_z(self, angle: float) -> Vec3:
		'''    Rotates the vector along the z axis'''
		pass

	def angle(self, other: Vec3):
		'''    Angle between two vectors'''
		pass

	def dot(self, other: Vec3) -> float:
		'''    Calculates dot product'''
		pass

	def clone(self) -> Vec3:
		'''    Clones vector'''
		pass

class Vec2:
	'''None'''

	@property
	def x(self) -> float:
		''''''
		pass

	@x.setter
	def x(self, value):
		''''''
		pass

	@property
	def y(self) -> float:
		''''''
		pass

	@y.setter
	def y(self, value):
		''''''
		pass

	def length(self) -> float:
		'''    '''
		pass

	def normalize(self) -> float:
		'''    '''
		pass

	def distance(self, other: Vec2) -> float:
		'''    '''
		pass

	def clone(self) -> Vec2:
		'''     Clones vector'''
		pass

class Summoner:
	'''Represents the type of a summoner spell'''

	Smite = 0
	Ignite = 1
	Cleanse = 2
	Teleport = 3
	Flash = 4
	HexFlash = 5
	Snowball = 6
	Clarity = 7
	Exhaust = 8
	Barrier = 9
	Heal = 10
	Ghost = 11
	Unknown = 12

class WindowFlag:
	'''Represents imgui window flags. These support bitwise operations so WindowFlag.NoResize | WindowFlag.NoMove would yield a flag with both'''

	NoFlags = 0
	NoTitleBar = 1
	NoResize = 2
	NoMove = 4
	NoScrollbar = 8
	NoScrollWithMouse = 16
	NoCollapse = 32
	AlwaysAutoResize = 64
	NoBackground = 128
	NoSavedSettings = 256
	NoMouseInputs = 512
	MenuBar = 1024
	HorizontalScrollbar = 2048
	NoFocusOnAppearing = 4096
	NoBringToFrontOnFocus = 8192
	AlwaysVerticalScrollbar = 16384
	AlwaysHorizontalScrollbar = 32768
	AlwaysUseWindowPadding = 65536
	NoNavInputs = 262144
	NoNavFocus = 524288
	UnsavedDocument = 1048576
	NoNav = 786432
	NoDecoration = 43
	NoInputs = 786944

class RayLayer:
	'''Represents the objects that a raycast can intercept'''

	Champion = 1
	Minion = 2
	Turret = 4
	Jungle = 8
	Missile = 16
	Other = 32
	Wall = 64
	Unit = 15
	All = 127
	Enemy = 256
	Ally = 128

class StyleVar:
	'''None'''

	Alpha = 0
	WindowPadding = 1
	WindowRounding = 2
	WindowBorderSize = 3
	WindowMinSize = 4
	WindowTitleAlign = 5
	ChildRounding = 6
	ChildBorderSize = 7
	PopupRounding = 8
	PopupBorderSize = 9
	FramePadding = 10
	FrameRounding = 11
	FrameBorderSize = 12
	ItemSpacing = 13
	ItemInnerSpacing = 14
	IndentSpacing = 15
	CellPadding = 16
	ScrollbarSize = 17
	ScrollbarRounding = 18
	GrabMinSize = 19
	GrabRounding = 20
	TabRounding = 21
	ButtonTextAlign = 22
	SelectableTextAlign = 23

	Alpha : any
	WindowPadding : any
	WindowRounding : any
	WindowBorderSize : any
	WindowMinSize : any
	WindowTitleAlign : any
	ChildRounding : any
	ChildBorderSize : any
	PopupRounding : any
	PopupBorderSize : any
	FramePadding : any
	FrameRounding : any
	FrameBorderSize : any
	ItemSpacing : any
	ItemInnerSpacing : any
	IndentSpacing : any
	CellPadding : any
	ScrollbarSize : any
	ScrollbarRounding : any
	GrabMinSize : any
	GrabRounding : any
	TabRounding : any
	ButtonTextAlign : any
	SelectableTextAlign : any
class Spell:
	'''Spell flags that specify behaviour and type of a spell'''

	CastPoint = 1
	CastAnywhere = 2
	CastTarget = 4
	CastDirection = 8
	TypeLine = 32
	TypeArea = 64
	TypeCone = 128
	CollideWindwall = 4096
	CollideMinion = 8192
	CollideChampion = 16384
	CollideMonster = 32768
	AffectMinion = 65536
	AffectChampion = 131072
	AffectMonster = 262144
	CollideCommon = 61440
	AffectAllUnits = 458752
	DashSkill = 524288
	ChannelSkill = 2097152
	ChargeableSkill = 1048576
	AppliesOnHit = 4194304

class Key:
	'''Hardware key codes'''

	no_key = 0
	esc = 1
	n1 = 2
	n2 = 3
	n3 = 4
	n4 = 5
	n5 = 6
	n6 = 7
	n7 = 8
	n8 = 9
	n9 = 10
	n0 = 11
	minus = 12
	equal = 13
	bs = 14
	tab = 15
	q = 16
	w = 17
	e = 18
	r = 19
	t = 20
	y = 21
	u = 22
	i = 23
	o = 24
	p = 25
	lbracket = 26
	rbracket = 27
	enter = 28
	ctrl = 29
	a = 30
	s = 31
	d = 32
	f = 33
	g = 34
	h = 35
	j = 36
	k = 37
	l = 38
	semicolon = 39
	single_quote = 40
	tilde = 41
	lshift = 42
	backslash = 43
	z = 44
	x = 45
	c = 46
	v = 47
	b = 48
	n = 49
	m = 50
	comma = 51
	dot = 52
	frontslash = 53
	rshift = 54
	print_screen = 55
	alt = 56
	space = 57
	caps = 58
	f1 = 59
	f2 = 60
	f3 = 61
	f4 = 62
	f5 = 63
	f6 = 64
	f7 = 65
	f8 = 66
	f9 = 67
	f10 = 68
	num = 69
	scroll = 70
	home = 71
	up = 72
	page_up = 73
	num_minus = 74
	left = 75
	center = 76
	right = 77
	plus = 78
	end = 79
	down = 80
	page_down = 81
	insert = 82
	delete = 83
	mouse_left = 84
	mouse_right = 85

class MapType:
	'''Map type SRU = Summoners Rift, HA = Howling Abyss'''

	SRU = 29299
	HA = 24936

class GameBuffType:
	'''Game buff type (use this instead of buffs from spells.py)'''

	Internal = 1
	Aura = 2
	CombatBuff = 3
	CombatDebuff = 4
	SpellShield = 5
	Stun = 6
	Invisibility = 7
	Silence = 8
	Taunt = 9
	Polymorph = 10
	Slow = 11
	Snare = 12
	Damage = 13
	Heal = 14
	Haste = 15
	SpellImmunity = 16
	PhysicalImmunity = 17
	Invulnerability = 18
	Sleep = 19
	NearSight = 20
	Frenzy = 21
	Fear = 22
	Charm = 23
	Poison = 24
	Suppression = 25
	Blind = 26
	Counter = 27
	Shred = 28
	Flee = 29
	Knockup = 30
	Knockback = 31
	Disarm = 32

class Unit:
	'''Riot unit tags extracted from the game files. These are not compatible with bitwise operations so writing things like Unit.Monster | Unit.Plant will not yield a tag that has both of those.'''

	Champion = 2
	ChampionClone = 3
	IsolationNonImpacting = 4
	KingPoro = 5
	Minion = 6
	MinionLane = 7
	MinionLaneMelee = 8
	MinionLaneRanged = 9
	MinionLaneSiege = 10
	MinionLaneSuper = 11
	MinionSummon = 12
	MinionSummon_Large = 14
	Monster = 15
	MonsterBlue = 16
	MonsterBuff = 17
	MonsterCamp = 18
	MonsterCrab = 19
	MonsterDragon = 20
	MonsterEpic = 21
	MonsterGromp = 22
	MonsterKrug = 23
	MonsterLarge = 24
	MonsterMedium = 25
	MonsterRaptor = 26
	MonsterRed = 27
	MonsterWolf = 28
	Plant = 29
	Special = 30
	SpecialAzirR = 31
	SpecialAzirW = 32
	SpecialCorkiBomb = 33
	SpecialEpicMonsterIgnores = 34
	SpecialKPMinion = 35
	SpecialMonsterIgnores = 36
	SpecialPeaceful = 37
	SpecialSyndraSphere = 38
	SpecialTeleportTarget = 39
	SpecialTrap = 40
	SpecialTunnel = 41
	SpecialTurretIgnores = 42
	SpecialUntargetableBySpells = 43
	SpecialVoid = 44
	SpecialYorickW = 45
	Structure = 46
	StructureInhibitor = 47
	StructureNexus = 48
	StructureTurret = 49
	StructureTurretInhib = 50
	StructureTurretInner = 51
	StructureTurretNexus = 52
	StructureTurretOuter = 53
	StructureTurretShrine = 54
	Ward = 55

class Map:
	'''Object representing the current game map'''

	@property
	def type(self) -> MapType:
		''' A enum value representing the currently played map'''
		pass

	@type.setter
	def type(self, value):
		''' A enum value representing the currently played map'''
		pass

class Keybind:
	'''Contains game keybinds'''

	cast_q : any
	cast_w : any
	cast_e : any
	cast_r : any
	cast_d : any
	cast_f : any
	use_item_1 : any
	use_item_2 : any
	use_item_3 : any
	use_item_4 : any
	use_item_5 : any
	use_item_6 : any
	use_trinket : any
	recall : any
	target_champ_only : any
class GameHud:
	'''Contains info about the hud in the game'''

	@property
	def minimap_pos(self) -> Vec2:
		''' Position of the minimap on the screen'''
		pass

	@minimap_pos.setter
	def minimap_pos(self, value):
		''' Position of the minimap on the screen'''
		pass

	@property
	def minimap_size(self) -> Vec2:
		''' Size of the minimap on the screen'''
		pass

	@minimap_size.setter
	def minimap_size(self, value):
		''' Size of the minimap on the screen'''
		pass

	@property
	def cursor_world_pos(self) -> Vec3:
		''' Position of mouse cursor in world coordinates'''
		pass

	@cursor_world_pos.setter
	def cursor_world_pos(self, value):
		''' Position of mouse cursor in world coordinates'''
		pass

	@property
	def chat_open(self) -> bool:
		''' True if chat is open'''
		pass

	@chat_open.setter
	def chat_open(self, value):
		''' True if chat is open'''
		pass

class RaycastResult:
	'''Represents the result of a raycast'''

	@property
	def point(self) -> Vec3:
		''' Point of raycast collision'''
		pass

	@point.setter
	def point(self, value):
		''' Point of raycast collision'''
		pass

	@property
	def obj(self) -> Obj:
		''' Object that the raycast collided with. None if it was a wall'''
		pass

	@obj.setter
	def obj(self, value):
		''' Object that the raycast collided with. None if it was a wall'''
		pass

class FutureCollision:
	'''Information about a future collision between a spell and a unit'''

	@property
	def spell(self) -> SpellCast:
		''' The spell in the collision'''
		pass

	@spell.setter
	def spell(self, value):
		''' The spell in the collision'''
		pass

	@property
	def unit(self) -> UnitObj:
		''' The unit in the collision'''
		pass

	@unit.setter
	def unit(self, value):
		''' The unit in the collision'''
		pass

	@property
	def unit_pos(self) -> Vec3:
		''' The unit position at the moment of collision'''
		pass

	@unit_pos.setter
	def unit_pos(self, value):
		''' The unit position at the moment of collision'''
		pass

	@property
	def spell_pos(self) -> Vec3:
		''' The spell position at the moment of collision'''
		pass

	@spell_pos.setter
	def spell_pos(self, value):
		''' The spell position at the moment of collision'''
		pass

	@property
	def final(self) -> bool:
		''' True if the projectile will not go further after this collision. Useful for drawing indicators'''
		pass

	@final.setter
	def final(self, value):
		''' True if the projectile will not go further after this collision. Useful for drawing indicators'''
		pass

	@property
	def time_until_impact(self) -> float:
		''' Time in seconds until the collision occurs'''
		pass

	@time_until_impact.setter
	def time_until_impact(self, value):
		''' Time in seconds until the collision occurs'''
		pass

class Buff:
	'''Contains data related to a buff on a champion'''

	@property
	def type(self) -> GameBuffType:
		''' Type of buff'''
		pass

	@type.setter
	def type(self, value):
		''' Type of buff'''
		pass

	@property
	def name(self) -> str:
		''' Name of the buff'''
		pass

	@name.setter
	def name(self, value):
		''' Name of the buff'''
		pass

	@property
	def time_begin(self) -> float:
		''' When the buff was received in game time'''
		pass

	@time_begin.setter
	def time_begin(self, value):
		''' When the buff was received in game time'''
		pass

	@property
	def time_end(self) -> float:
		''' When the buff will end in game time'''
		pass

	@time_end.setter
	def time_end(self, value):
		''' When the buff will end in game time'''
		pass

	@property
	def count(self) -> int:
		''' Number of stacks of the buff'''
		pass

	@count.setter
	def count(self, value):
		''' Number of stacks of the buff'''
		pass

	@property
	def value(self) -> int:
		''' Value of the buff'''
		pass

	@value.setter
	def value(self, value):
		''' Value of the buff'''
		pass

class UnitStatic:
	'''Static data loaded at runtime for an unit'''

	@property
	def hp_bar_height(self) -> float:
		''' The height at which the health bar starts'''
		pass

	@hp_bar_height.setter
	def hp_bar_height(self, value):
		''' The height at which the health bar starts'''
		pass

	@property
	def movement_speed(self) -> float:
		''' Base movement speed'''
		pass

	@movement_speed.setter
	def movement_speed(self, value):
		''' Base movement speed'''
		pass

	@property
	def base_atk_range(self) -> float:
		''' Base attack range'''
		pass

	@base_atk_range.setter
	def base_atk_range(self, value):
		''' Base attack range'''
		pass

	@property
	def base_atk_speed(self) -> float:
		''' Base attack speed'''
		pass

	@base_atk_speed.setter
	def base_atk_speed(self, value):
		''' Base attack speed'''
		pass

	@property
	def atk_speed_ratio(self) -> float:
		''' Attack speed ratio'''
		pass

	@atk_speed_ratio.setter
	def atk_speed_ratio(self, value):
		''' Attack speed ratio'''
		pass

	@property
	def acquisition_radius(self) -> float:
		''' Acquisition radius. See league wiki for more info'''
		pass

	@acquisition_radius.setter
	def acquisition_radius(self, value):
		''' Acquisition radius. See league wiki for more info'''
		pass

	@property
	def selection_radius(self) -> float:
		''' Selection radius. See league wiki for more info'''
		pass

	@selection_radius.setter
	def selection_radius(self, value):
		''' Selection radius. See league wiki for more info'''
		pass

	@property
	def pathing_radius(self) -> float:
		''' Pathing radius. See league wiki for more info'''
		pass

	@pathing_radius.setter
	def pathing_radius(self, value):
		''' Pathing radius. See league wiki for more info'''
		pass

	@property
	def gameplay_radius(self) -> float:
		''' Gameplay radius. See league wiki for more info'''
		pass

	@gameplay_radius.setter
	def gameplay_radius(self, value):
		''' Gameplay radius. See league wiki for more info'''
		pass

	@property
	def basic_atk(self) -> SpellStatic:
		''' Default basic attack on the unit'''
		pass

	@basic_atk.setter
	def basic_atk(self, value):
		''' Default basic attack on the unit'''
		pass

	@property
	def basic_atk_windup(self) -> float:
		''' Basic attack windup. See league wiki for more info'''
		pass

	@basic_atk_windup.setter
	def basic_atk_windup(self, value):
		''' Basic attack windup. See league wiki for more info'''
		pass

	@property
	def basic_atk_cast_time(self) -> float:
		''' Basic attack cast time. See league wiki for more info'''
		pass

	@basic_atk_cast_time.setter
	def basic_atk_cast_time(self, value):
		''' Basic attack cast time. See league wiki for more info'''
		pass

class ItemSlot:
	'''Represents an item slot'''

	@property
	def charges(self) -> int:
		''' Charges of item (example: corruption potion charges, number of red potions etc)'''
		pass

	@charges.setter
	def charges(self, value):
		''' Charges of item (example: corruption potion charges, number of red potions etc)'''
		pass

	@property
	def item(self) -> ItemStatic:
		''' Static data of the item. If there is no item on the slot then this is None otherwise it is an ItemStatic instance'''
		pass

	@item.setter
	def item(self, value):
		''' Static data of the item. If there is no item on the slot then this is None otherwise it is an ItemStatic instance'''
		pass

	@property
	def active(self) -> SpellObj:
		''' Spell active of the item. None if item doesnt have active'''
		pass

	@active.setter
	def active(self, value):
		''' Spell active of the item. None if item doesnt have active'''
		pass

class ItemStatic:
	'''Static data loaded at runtime for an item'''

	@property
	def id(self) -> int:
		''' Item internal id'''
		pass

	@id.setter
	def id(self, value):
		''' Item internal id'''
		pass

	@property
	def cost(self) -> float:
		''' Cost of item in gold coins'''
		pass

	@cost.setter
	def cost(self, value):
		''' Cost of item in gold coins'''
		pass

	@property
	def mov_speed(self) -> float:
		''' Flat movement speed given by item'''
		pass

	@mov_speed.setter
	def mov_speed(self, value):
		''' Flat movement speed given by item'''
		pass

	@property
	def health(self) -> float:
		''' Flat health given by item'''
		pass

	@health.setter
	def health(self, value):
		''' Flat health given by item'''
		pass

	@property
	def crit(self) -> float:
		''' Crit chance given by item'''
		pass

	@crit.setter
	def crit(self, value):
		''' Crit chance given by item'''
		pass

	@property
	def ap(self) -> float:
		''' Flat ability power given by item'''
		pass

	@ap.setter
	def ap(self, value):
		''' Flat ability power given by item'''
		pass

	@property
	def mana(self) -> float:
		''' Flat mana given by item'''
		pass

	@mana.setter
	def mana(self, value):
		''' Flat mana given by item'''
		pass

	@property
	def armor(self) -> float:
		''' Flat armour given by item'''
		pass

	@armor.setter
	def armor(self, value):
		''' Flat armour given by item'''
		pass

	@property
	def magic_res(self) -> float:
		''' Flat magic resist given by item'''
		pass

	@magic_res.setter
	def magic_res(self, value):
		''' Flat magic resist given by item'''
		pass

	@property
	def phys_dmg(self) -> float:
		''' Flat physical damage given by item'''
		pass

	@phys_dmg.setter
	def phys_dmg(self, value):
		''' Flat physical damage given by item'''
		pass

	@property
	def atk_speed(self) -> float:
		''' Attack speed percent given by item'''
		pass

	@atk_speed.setter
	def atk_speed(self, value):
		''' Attack speed percent given by item'''
		pass

	@property
	def life_steal(self) -> float:
		''' Life steal percent given by item'''
		pass

	@life_steal.setter
	def life_steal(self, value):
		''' Life steal percent given by item'''
		pass

	@property
	def hp_regen(self) -> float:
		''' Health regen percent given by item'''
		pass

	@hp_regen.setter
	def hp_regen(self, value):
		''' Health regen percent given by item'''
		pass

	@property
	def mov_speed_percent(self) -> float:
		''' Movement speed percent given by item'''
		pass

	@mov_speed_percent.setter
	def mov_speed_percent(self, value):
		''' Movement speed percent given by item'''
		pass

class SpellStatic:
	'''Static data loaded at runtime for a spell'''

	@property
	def name(self) -> str:
		''' Name of the spell in lower case'''
		pass

	@name.setter
	def name(self, value):
		''' Name of the spell in lower case'''
		pass

	@property
	def icon(self) -> str:
		''' Icon name of the spell in lowercase'''
		pass

	@icon.setter
	def icon(self, value):
		''' Icon name of the spell in lowercase'''
		pass

	@property
	def cast_time(self) -> float:
		''' Cast time of spell'''
		pass

	@cast_time.setter
	def cast_time(self, value):
		''' Cast time of spell'''
		pass

	@property
	def cast_range(self) -> float:
		''' Cast range of the spell. Can mean multiple things, the range of a skillshot or the cast range of targeted spell'''
		pass

	@cast_range.setter
	def cast_range(self, value):
		''' Cast range of the spell. Can mean multiple things, the range of a skillshot or the cast range of targeted spell'''
		pass

	@property
	def cast_radius(self) -> float:
		''' Cast radius of the spell (e.g Ziggs R area of effect)'''
		pass

	@cast_radius.setter
	def cast_radius(self, value):
		''' Cast radius of the spell (e.g Ziggs R area of effect)'''
		pass

	@property
	def cast_cone_angle(self) -> float:
		''' If spell is conic this is the cone angle'''
		pass

	@cast_cone_angle.setter
	def cast_cone_angle(self, value):
		''' If spell is conic this is the cone angle'''
		pass

	@property
	def cast_cone_distance(self) -> float:
		''' If the spell is conic this is the cone length'''
		pass

	@cast_cone_distance.setter
	def cast_cone_distance(self, value):
		''' If the spell is conic this is the cone length'''
		pass

	@property
	def delay(self) -> float:
		''' Additional delay besides the cast_time. Also if a missile has fixed travel time the value will be added here.'''
		pass

	@delay.setter
	def delay(self, value):
		''' Additional delay besides the cast_time. Also if a missile has fixed travel time the value will be added here.'''
		pass

	@property
	def width(self) -> float:
		''' Width of the spell'''
		pass

	@width.setter
	def width(self, value):
		''' Width of the spell'''
		pass

	@property
	def height_augment(self) -> float:
		''' For drawing purposes. Height of the missile/spell must be augmented by this value'''
		pass

	@height_augment.setter
	def height_augment(self, value):
		''' For drawing purposes. Height of the missile/spell must be augmented by this value'''
		pass

	@property
	def speed(self) -> float:
		''' Speed of the spell. Used mostly by missile spells'''
		pass

	@speed.setter
	def speed(self, value):
		''' Speed of the spell. Used mostly by missile spells'''
		pass

	def has_flag(self, flag: Spell) -> bool:
		'''     Checks if the spell has the specified Spell flag'''
		pass

class Obj:
	'''Represents the base of a ingame object. Most ingame objects derive from this.'''

	@property
	def name(self) -> str:
		''' Name of the object in lower case'''
		pass

	@name.setter
	def name(self, value):
		''' Name of the object in lower case'''
		pass

	@property
	def index(self) -> int:
		''' Index of the object. This is not a unique id, you use this for targeted spells to find who the target is'''
		pass

	@index.setter
	def index(self, value):
		''' Index of the object. This is not a unique id, you use this for targeted spells to find who the target is'''
		pass

	@property
	def net_id(self) -> int:
		''' Network id. This is a unique id of the object'''
		pass

	@net_id.setter
	def net_id(self, value):
		''' Network id. This is a unique id of the object'''
		pass

	@property
	def team(self) -> int:
		''' Team of the object: possible values 100, 200 and 300 for jungle side. Use ally_to/enemy_to functions instead of this'''
		pass

	@team.setter
	def team(self, value):
		''' Team of the object: possible values 100, 200 and 300 for jungle side. Use ally_to/enemy_to functions instead of this'''
		pass

	@property
	def pos(self) -> Vec3:
		''' Position of the object'''
		pass

	@pos.setter
	def pos(self, value):
		''' Position of the object'''
		pass

	@property
	def visible(self) -> bool:
		''' True if object is visible'''
		pass

	@visible.setter
	def visible(self, value):
		''' True if object is visible'''
		pass

	@property
	def last_seen(self) -> float:
		''' Timestamp in game time for when the object was last visible'''
		pass

	@last_seen.setter
	def last_seen(self, value):
		''' Timestamp in game time for when the object was last visible'''
		pass

	@property
	def first_seen(self) -> float:
		''' When the object was first seen'''
		pass

	@first_seen.setter
	def first_seen(self, value):
		''' When the object was first seen'''
		pass

	@property
	def dir(self) -> Vec3:
		''' Direction the object is facing as a normalized Vec3'''
		pass

	@dir.setter
	def dir(self, value):
		''' Direction the object is facing as a normalized Vec3'''
		pass

	@property
	def bounding_radius(self) -> float:
		''' The bounding radius of the object a.k.a the hitbox (but its actually a circle)'''
		pass

	@bounding_radius.setter
	def bounding_radius(self, value):
		''' The bounding radius of the object a.k.a the hitbox (but its actually a circle)'''
		pass

	def in_front_of(self, other: Obj) -> bool:
		'''    Checks if object is in front of another object'''
		pass

	def ally_to(self, other: Obj) -> bool:
		'''    Checks if two objects are allied'''
		pass

	def enemy_to(self, other: Obj) -> bool:
		'''    Checks if two objects are enemies'''
		pass

	def menu_draw(self) -> bool:
		'''    Draws the object in the current menu'''
		pass

class SpellObj:
	'''Represents a spell in game. In case of spells from items make sure level > 0 before casting it.'''

	@property
	def name(self) -> str:
		''' Name of the spell in lower case'''
		pass

	@name.setter
	def name(self, value):
		''' Name of the spell in lower case'''
		pass

	@property
	def lvl(self) -> int:
		''' Level of the spell. Has value 0 when spell is not learned'''
		pass

	@lvl.setter
	def lvl(self, value):
		''' Level of the spell. Has value 0 when spell is not learned'''
		pass

	@property
	def ready_at(self) -> float:
		''' Timestamp in game time for when the cooldown of the spell ends'''
		pass

	@ready_at.setter
	def ready_at(self, value):
		''' Timestamp in game time for when the cooldown of the spell ends'''
		pass

	@property
	def value(self) -> float:
		''' Value of spells. Holds the value of the spell for summoner spells like ignite/smite it holds the damage. For champion spells this value is usually 0'''
		pass

	@value.setter
	def value(self, value):
		''' Value of spells. Holds the value of the spell for summoner spells like ignite/smite it holds the damage. For champion spells this value is usually 0'''
		pass

	@property
	def cd(self) -> float:
		''' The remaining cooldown of the spell. Internally it is calculated using ready_at'''
		pass

	@cd.setter
	def cd(self, value):
		''' The remaining cooldown of the spell. Internally it is calculated using ready_at'''
		pass

	@property
	def mana(self) -> float:
		''' Mana necessarry for casting the spell'''
		pass

	@mana.setter
	def mana(self, value):
		''' Mana necessarry for casting the spell'''
		pass

	@property
	def static(self) -> SpellStatic:
		''' Gets static information loaded at runtime about the spell. Can be None but normally shouldn't. If you find a object for which this is null please contact a dev'''
		pass

	@static.setter
	def static(self, value):
		''' Gets static information loaded at runtime about the spell. Can be None but normally shouldn't. If you find a object for which this is null please contact a dev'''
		pass

	@property
	def key(self) -> Key:
		''' Key bound to this spell'''
		pass

	@key.setter
	def key(self, value):
		''' Key bound to this spell'''
		pass

class SummonerSpell(SpellObj):
	'''Represents a summoner spell'''

	type : any
class SpellCast:
	'''Has data about a spell being cast.'''

	@property
	def start_pos(self) -> Vec3:
		''' Start position of the spell. Usually the position of the caster'''
		pass

	@start_pos.setter
	def start_pos(self, value):
		''' Start position of the spell. Usually the position of the caster'''
		pass

	@property
	def end_pos(self) -> Vec3:
		''' End position of the spell. Use this to get the direction of the spell. Remarks: this might not always be the real endpoint check SpellStatic project_endpoint field for more information.'''
		pass

	@end_pos.setter
	def end_pos(self, value):
		''' End position of the spell. Use this to get the direction of the spell. Remarks: this might not always be the real endpoint check SpellStatic project_endpoint field for more information.'''
		pass

	@property
	def dir(self) -> Vec3:
		''' Direction the spell is facing (in case of missiles)'''
		pass

	@dir.setter
	def dir(self, value):
		''' Direction the spell is facing (in case of missiles)'''
		pass

	@property
	def src_index(self) -> int:
		''' Index of the object who is casting'''
		pass

	@src_index.setter
	def src_index(self, value):
		''' Index of the object who is casting'''
		pass

	@property
	def dest_index(self) -> int:
		''' If casting a targeted spell this holds the index of the target object'''
		pass

	@dest_index.setter
	def dest_index(self, value):
		''' If casting a targeted spell this holds the index of the target object'''
		pass

	@property
	def time_begin(self) -> float:
		''' Start timestamp in game time of the casting'''
		pass

	@time_begin.setter
	def time_begin(self, value):
		''' Start timestamp in game time of the casting'''
		pass

	@property
	def cast_time(self) -> float:
		''' Total cast time'''
		pass

	@cast_time.setter
	def cast_time(self, value):
		''' Total cast time'''
		pass

	@property
	def remaining(self) -> float:
		''' Remaining cast time. This can go into negatives since casts arent removed from memory always'''
		pass

	@remaining.setter
	def remaining(self, value):
		''' Remaining cast time. This can go into negatives since casts arent removed from memory always'''
		pass

	@property
	def static(self) -> SpellStatic:
		''' Static data of the spell being cast. Can be None but normally shouldn't. If you find a object for which this is null please contact a dev'''
		pass

	@static.setter
	def static(self, value):
		''' Static data of the spell being cast. Can be None but normally shouldn't. If you find a object for which this is null please contact a dev'''
		pass

	@property
	def name(self) -> str:
		''' Name of the spell being cast'''
		pass

	@name.setter
	def name(self, value):
		''' Name of the spell being cast'''
		pass

class MissileObj(Obj):
	'''None'''

	@property
	def spell(self) -> SpellCast:
		''' The spell of the missile. A spell can have multiple missiles. So this is not necessarily the spell that was cast.'''
		pass

	@spell.setter
	def spell(self, value):
		''' The spell of the missile. A spell can have multiple missiles. So this is not necessarily the spell that was cast.'''
		pass

class UnitObj(Obj):
	'''Represents a base unit object'''

	@property
	def dead(self) -> bool:
		''' Used to check if unit is dead'''
		pass

	@dead.setter
	def dead(self, value):
		''' Used to check if unit is dead'''
		pass

	@property
	def targetable(self) -> bool:
		''' Used to check if unit is targetable'''
		pass

	@targetable.setter
	def targetable(self, value):
		''' Used to check if unit is targetable'''
		pass

	@property
	def invulnerable(self) -> bool:
		''' Used to check if unit is invulnerable'''
		pass

	@invulnerable.setter
	def invulnerable(self, value):
		''' Used to check if unit is invulnerable'''
		pass

	@property
	def mana(self) -> float:
		''' Current mana of the unit'''
		pass

	@mana.setter
	def mana(self, value):
		''' Current mana of the unit'''
		pass

	@property
	def max_mana(self) -> float:
		''' Max mana of the unit'''
		pass

	@max_mana.setter
	def max_mana(self, value):
		''' Max mana of the unit'''
		pass

	@property
	def health(self) -> float:
		''' Current health of the unit'''
		pass

	@health.setter
	def health(self, value):
		''' Current health of the unit'''
		pass

	@property
	def max_health(self) -> float:
		''' Max health of the unit'''
		pass

	@max_health.setter
	def max_health(self, value):
		''' Max health of the unit'''
		pass

	@property
	def armor(self) -> float:
		''' Total armor of the unit'''
		pass

	@armor.setter
	def armor(self, value):
		''' Total armor of the unit'''
		pass

	@property
	def magic_res(self) -> float:
		''' Total magic resist of the unit'''
		pass

	@magic_res.setter
	def magic_res(self, value):
		''' Total magic resist of the unit'''
		pass

	@property
	def atk(self) -> float:
		''' Total attack damage of the unit'''
		pass

	@atk.setter
	def atk(self, value):
		''' Total attack damage of the unit'''
		pass

	@property
	def lethality(self) -> float:
		''' Lethality of unit'''
		pass

	@lethality.setter
	def lethality(self, value):
		''' Lethality of unit'''
		pass

	@property
	def haste(self) -> float:
		''' Haste of unit'''
		pass

	@haste.setter
	def haste(self, value):
		''' Haste of unit'''
		pass

	@property
	def cdr(self) -> float:
		''' Cooldown reduction of unit'''
		pass

	@cdr.setter
	def cdr(self, value):
		''' Cooldown reduction of unit'''
		pass

	@property
	def base_atk(self) -> float:
		''' Base physical damage of the unit'''
		pass

	@base_atk.setter
	def base_atk(self, value):
		''' Base physical damage of the unit'''
		pass

	@property
	def move_speed(self) -> float:
		''' Movement speed of the unit'''
		pass

	@move_speed.setter
	def move_speed(self, value):
		''' Movement speed of the unit'''
		pass

	@property
	def lvl(self) -> int:
		''' Level of the unit'''
		pass

	@lvl.setter
	def lvl(self, value):
		''' Level of the unit'''
		pass

	@property
	def expiry(self) -> float:
		''' Expiration duration in seconds. Used for units like wards'''
		pass

	@expiry.setter
	def expiry(self, value):
		''' Expiration duration in seconds. Used for units like wards'''
		pass

	@property
	def crit(self) -> float:
		''' Crit chance of the unit as a decimal'''
		pass

	@crit.setter
	def crit(self, value):
		''' Crit chance of the unit as a decimal'''
		pass

	@property
	def crit_multi(self) -> float:
		''' Crit multi of the unit as a decimal'''
		pass

	@crit_multi.setter
	def crit_multi(self, value):
		''' Crit multi of the unit as a decimal'''
		pass

	@property
	def ap(self) -> float:
		''' Flat ability power of the unit'''
		pass

	@ap.setter
	def ap(self, value):
		''' Flat ability power of the unit'''
		pass

	@property
	def atk_speed_multi(self) -> float:
		''' Attack speed multiplier of the unit as a decimal. Multiply this with base attack speed to get current attack speed'''
		pass

	@atk_speed_multi.setter
	def atk_speed_multi(self, value):
		''' Attack speed multiplier of the unit as a decimal. Multiply this with base attack speed to get current attack speed'''
		pass

	@property
	def atk_range(self) -> float:
		''' Attack range of the unit'''
		pass

	@atk_range.setter
	def atk_range(self, value):
		''' Attack range of the unit'''
		pass

	@property
	def atk_speed(self) -> float:
		''' Calculates the attack speed of the unit'''
		pass

	@atk_speed.setter
	def atk_speed(self, value):
		''' Calculates the attack speed of the unit'''
		pass

	@property
	def bonus_move_speed(self) -> float:
		''' Bonus move speed of unit'''
		pass

	@bonus_move_speed.setter
	def bonus_move_speed(self, value):
		''' Bonus move speed of unit'''
		pass

	@property
	def bonus_armor(self) -> float:
		''' Bonus armor of the unit'''
		pass

	@bonus_armor.setter
	def bonus_armor(self, value):
		''' Bonus armor of the unit'''
		pass

	@property
	def bonus_magic_res(self) -> float:
		''' Bonus magic resist of the unit'''
		pass

	@bonus_magic_res.setter
	def bonus_magic_res(self, value):
		''' Bonus magic resist of the unit'''
		pass

	@property
	def bonus_atk(self) -> float:
		''' Bonus physical damage of the unit (from items, buffs etc)'''
		pass

	@bonus_atk.setter
	def bonus_atk(self, value):
		''' Bonus physical damage of the unit (from items, buffs etc)'''
		pass

	@property
	def bonus_atk_speed(self) -> float:
		''' Bonus attack speed of the unit'''
		pass

	@bonus_atk_speed.setter
	def bonus_atk_speed(self, value):
		''' Bonus attack speed of the unit'''
		pass

	@property
	def curr_casting(self) -> SpellCast:
		''' Currently casting spell by the unit'''
		pass

	@curr_casting.setter
	def curr_casting(self, value):
		''' Currently casting spell by the unit'''
		pass

	@property
	def static(self) -> UnitStatic:
		''' Static data loaded at runtime of the unit. Can be None but normally shouldn't. If you find a object for which this is null please contact a dev'''
		pass

	@static.setter
	def static(self, value):
		''' Static data loaded at runtime of the unit. Can be None but normally shouldn't. If you find a object for which this is null please contact a dev'''
		pass

	@property
	def is_ranged(self) -> bool:
		''' True if unit is ranged'''
		pass

	@is_ranged.setter
	def is_ranged(self, value):
		''' True if unit is ranged'''
		pass

	@property
	def buffs(self) -> list[Buff]:
		''' List of all the buffs on the champion. Currently buffs are only read for the player champion and enemies due to performance reasons.'''
		pass

	@buffs.setter
	def buffs(self, value):
		''' List of all the buffs on the champion. Currently buffs are only read for the player champion and enemies due to performance reasons.'''
		pass

	@property
	def moving(self) -> bool:
		''' True if unit is moving'''
		pass

	@moving.setter
	def moving(self, value):
		''' True if unit is moving'''
		pass

	@property
	def dashing(self) -> bool:
		''' True if unit is dashing'''
		pass

	@dashing.setter
	def dashing(self, value):
		''' True if unit is dashing'''
		pass

	@property
	def dash_speed(self) -> float:
		''' Similar to move speed but when dashing'''
		pass

	@dash_speed.setter
	def dash_speed(self, value):
		''' Similar to move speed but when dashing'''
		pass

	@property
	def path(self) -> list[Vec3]:
		''' Navigation path of the unit'''
		pass

	@path.setter
	def path(self, value):
		''' Navigation path of the unit'''
		pass

	@property
	def destination(self) -> Vec3:
		''' Navigation destination of the unit'''
		pass

	@destination.setter
	def destination(self, value):
		''' Navigation destination of the unit'''
		pass

	def get_buff(self, name : str) -> Buff:
		'''    Gets the buff with the name provided or None if nothing found'''
		pass

	def num_buff_stacks(self, name : str) -> int:
		'''    Gets the number of stacks for the buff given by the name'''
		pass

	def effective_phys_dmg(self, target: UnitObj, raw_dmg: float) -> float:
		'''    Calculates effective physical damage against target considering armor and armor penetration'''
		pass

	def effective_magic_dmg(self, target: UnitObj, raw_dmg: float) -> float:
		'''    Calculates effective magic damage against target considering magic res and magic res penetration'''
		pass

	def has_tags(self, tag_flag: Unit) -> bool:
		'''    Checks if the unit has unit tags (see Unit class)'''
		pass

	def path_distance(self) -> float:
		'''    Calculates navigation path distance in game units'''
		pass

	def predict_position(self, time_future: float) -> float:
		'''    Predicts position of unit in X seconds'''
		pass

	def reskin(self, id: int):
		'''    Changes the skin of the unit'''
		pass

	def has_buff(self, buff: str) -> bool:
		'''    Check if champion has buff. The buff name is case sensitive'''
		pass

class ChampionObj(UnitObj):
	'''Represents a champion object'''

	def get_summoner(type: Summoner) -> SummonerSpell:
		'''    Gets the summoner spell with the specified type. Returns None if player doesnt have that summoner spell'''
		pass

	def can_cast_spell(self, spell: SpellObj) -> bool:
		'''    Checks if champion can cast the GameSpell provided'''
		pass

	def has_item(self, item_id: int) -> bool:
		'''    Check if champion has item with item id'''
		pass

	def get_item(self, item_id: int) -> ItemSlot:
		'''    Gets item slot that contains the item with the given id. If no item is found None is returned'''
		pass

	@property
	def spells(self) -> list[SpellObj]:
		''' List of all the champion spells. Remarks: First 4 spells are Q,W,E,R. Next two are D,F.The next 6 are item spells. Use Context.cast_spell to cast them. Only enemies and local player have item actives read for performance reasons'''
		pass

	@spells.setter
	def spells(self, value):
		''' List of all the champion spells. Remarks: First 4 spells are Q,W,E,R. Next two are D,F.The next 6 are item spells. Use Context.cast_spell to cast them. Only enemies and local player have item actives read for performance reasons'''
		pass

	@property
	def item_slots(self) -> list[ItemSlot]:
		''' List of inventory slots. If an item is on the slot then the value is an Item object otherwise None. Only local player and enemies have items read for performance reasons'''
		pass

	@item_slots.setter
	def item_slots(self, value):
		''' List of inventory slots. If an item is on the slot then the value is an Item object otherwise None. Only local player and enemies have items read for performance reasons'''
		pass

	@property
	def Q(self) -> SpellObj:
		''' Get Q spell'''
		pass

	@Q.setter
	def Q(self, value):
		''' Get Q spell'''
		pass

	@property
	def W(self) -> SpellObj:
		''' Get W spell'''
		pass

	@W.setter
	def W(self, value):
		''' Get W spell'''
		pass

	@property
	def E(self) -> SpellObj:
		''' Get E spell'''
		pass

	@E.setter
	def E(self, value):
		''' Get E spell'''
		pass

	@property
	def R(self) -> SpellObj:
		''' Get R spell'''
		pass

	@R.setter
	def R(self, value):
		''' Get R spell'''
		pass

	@property
	def hpbar_pos(self) -> float:
		''' Height position of the HP bar of the champion'''
		pass

	@hpbar_pos.setter
	def hpbar_pos(self, value):
		''' Height position of the HP bar of the champion'''
		pass

	@property
	def recalling(self) -> bool:
		''' True if champion is recalling'''
		pass

	@recalling.setter
	def recalling(self, value):
		''' True if champion is recalling'''
		pass

	@property
	def recall_start_time(self) -> float:
		''' Start time of the recall in game time. Use this only if recalling flag is True'''
		pass

	@recall_start_time.setter
	def recall_start_time(self, value):
		''' Start time of the recall in game time. Use this only if recalling flag is True'''
		pass

	@property
	def is_clone(self) -> bool:
		''' Checks if the champion is a clone'''
		pass

	@is_clone.setter
	def is_clone(self, value):
		''' Checks if the champion is a clone'''
		pass

	@property
	def channeling(self) -> bool:
		''' True if player is channeling a spell'''
		pass

	@channeling.setter
	def channeling(self, value):
		''' True if player is channeling a spell'''
		pass

class TurretObj(UnitObj):
	'''Represents a turret object'''

class MinionObj(UnitObj):
	'''Represents a minion object'''

	@property
	def hpbar_pos(self) -> float:
		''' Height position of the HP bar of the minion'''
		pass

	@hpbar_pos.setter
	def hpbar_pos(self, value):
		''' Height position of the HP bar of the minion'''
		pass

class JungleMobObj(UnitObj):
	'''Represents a jungle mob object'''

class UI:
	'''Used to draw imgui backed UIs. Each method is more or less the equivalent of the original imgui method. Check imgui documentation for more info'''

	def begin(self, name: str):
		'''    '''
		pass

	def beginchild(self, name: str, flags: WindowFlag):
		'''    '''
		pass

	def endchild(self):
		'''    '''
		pass

	def end(self):
		'''    '''
		pass

	def pushvar(self, style: StyleVar, value: Vec2):
		'''    '''
		pass

	def popvar(self, style: StyleVar):
		'''    '''
		pass

	def help(self, msg: str):
		'''     Shows a help market in front of the next widget'''
		pass

	def button(self, txt: str) -> bool:
		'''     '''
		pass

	def colorpick(self, txt: str, color: Col) -> Col:
		'''     '''
		pass

	def checkbox(self, txt: str, checked: bool) -> bool:
		'''     '''
		pass

	def text(self, txt: str):
		'''     '''
		pass

	def text_color(self, txt: str, color: Col):
		'''     '''
		pass

	def labeltext(self, label: str, txt: str):
		'''     '''
		pass

	def separator(self):
		'''     '''
		pass

	def dragint(self, txt: str, value: int, step: int, min_val: int, max_val: int) -> int:
		'''     '''
		pass

	def dragfloat(self, txt: str, value: float, step: float, min_val: float, max_val: float) -> float:
		'''     '''
		pass

	def keyselect(self, txt: str, key, Key) -> Key:
		'''     '''
		pass

	def sliderfloat(self, txt: str, value: float, min_val: float, max_val: float) -> float:
		'''     '''
		pass

	def sliderint(self, txt: str, value: int, min_val: int, max_val: int) -> int:
		'''     '''
		pass

	def sliderenum(self, txt: str, selected_name: str, selected: int, max_select: int) -> int:
		'''     '''
		pass

	def progressbar(self, fraction: float, size: Vec2, text: str):
		'''     '''
		pass

	def image(self, id: str, size: Vec2, color: Col):
		'''     Draws an image in the menu'''
		pass

	def header(self, text: str) -> bool:
		'''    '''
		pass

	def treenode(self, text: str) -> bool:
		'''    '''
		pass

	def treepop(self):
		'''    '''
		pass

	def beginmenu(self, text: str) -> bool:
		'''    '''
		pass

	def endmenu(self):
		'''    '''
		pass

	def opennext(self):
		'''    '''
		pass

	def openpopup(self, popup: str):
		'''    '''
		pass

	def beginpopup(self, text: str) -> bool:
		'''    '''
		pass

	def endpopup(self):
		'''    '''
		pass

	def beginmodal(self, text: str) -> bool:
		'''    '''
		pass

	def closepopup(self):
		'''    '''
		pass

	def selectable(self, text: str) -> bool:
		'''    '''
		pass

	def begintbl(self, text: str, num_columns: int) -> bool:
		'''    '''
		pass

	def endtbl(self):
		'''    '''
		pass

	def tblnextrow(self):
		'''    '''
		pass

	def tblcolumn(self, column: int):
		'''    '''
		pass

	def inputtext(self, label: str, input: str) -> str:
		'''    '''
		pass

	def sameline(self):
		'''    '''
		pass

	def begingroup(self):
		'''    '''
		pass

	def endgroup(self):
		'''    '''
		pass

	def listbox(self, items: list[str], current: int) -> int:
		'''     '''
		pass

	def combo(self, items: list[str], current: int) -> int:
		'''     '''
		pass

	def demo(self):
		'''     Shows the famous imgui demo'''
		pass

	def pushid(self, id: int):
		'''     '''
		pass

	def popid(self):
		'''     '''
		pass

	def indent(self, space: float):
		'''     '''
		pass

class ObjectQuery:
	'''Used to query game objects by avoiding python to C++ call overhead.'''

	def get(self) -> list[Obj]:
		'''     Returns the objects from the query'''
		pass

	def count(self) -> int:
		'''     Makes the query but returns just the number of objects'''
		pass

	def has_tag(self, tag: Unit) -> ObjectQuery:
		'''    Query units with specified tag'''
		pass

	def ally_to(self, other: Obj) -> ObjectQuery:
		'''    Query allies'''
		pass

	def enemy_to(self, other: Obj) -> ObjectQuery:
		'''    Query enemies'''
		pass

	def near(self, obj: Obj) -> ObjectQuery:
		'''    Query objects within distance of another object'''
		pass

	def targetable(self) -> ObjectQuery:
		'''    Query targetable. Not equivalent to UnitObj.targetable. This checks if obj is alive, targetable and not invulnerable'''
		pass

	def untargetable(self) -> ObjectQuery:
		'''    Query untargetable'''
		pass

	def visible(self) -> ObjectQuery:
		'''    Query objects in vision'''
		pass

	def invisible(self) -> ObjectQuery:
		'''    Query objects out of vision'''
		pass

	def alive(self) -> ObjectQuery:
		'''    Query alive objects'''
		pass

	def dead(self) -> ObjectQuery:
		'''    Query dead objects'''
		pass

	def clone(self) -> ObjectQuery:
		'''    Query clone objects'''
		pass

	def not_clone(self) -> ObjectQuery:
		'''    Query non clone objects'''
		pass

	def on_screen(self) -> ObjectQuery:
		'''    Query objects on screen'''
		pass

	def casting(self) -> ObjectQuery:
		'''    Query units casting a spell'''
		pass

class Context:
	'''Contains everything necessarry to create scripts. From utility functions to game data'''

	def info(self, msg: str):
		'''    Logs an info message to the console & file log'''
		pass

	def warn(self, msg: str):
		'''    Logs a warning message to the console & file log'''
		pass

	def error(self, msg: str):
		'''    Logs a error message to the console & file log. The file log will be flushed. Use this in absolute worse cases'''
		pass

	@property
	def resources_loaded(self) -> bool:
		''' True if all valkyrie resources are loaded (images/jsons etc)'''
		pass

	@resources_loaded.setter
	def resources_loaded(self, value):
		''' True if all valkyrie resources are loaded (images/jsons etc)'''
		pass

	@property
	def ui(self) -> UI:
		''' UI interface for drawing menus based on imgui'''
		pass

	@ui.setter
	def ui(self, value):
		''' UI interface for drawing menus based on imgui'''
		pass

	@property
	def cfg(self) -> Config:
		''' The script config interface. Used to load/save settings'''
		pass

	@cfg.setter
	def cfg(self, value):
		''' The script config interface. Used to load/save settings'''
		pass

	@property
	def time(self) -> float:
		''' Current game duration in seconds'''
		pass

	@time.setter
	def time(self, value):
		''' Current game duration in seconds'''
		pass

	@property
	def ping(self) -> float:
		''' Current ping of the game'''
		pass

	@ping.setter
	def ping(self, value):
		''' Current ping of the game'''
		pass

	@property
	def cursor_pos(self) -> Vec2:
		''' Gets the current position of the mouse'''
		pass

	@cursor_pos.setter
	def cursor_pos(self, value):
		''' Gets the current position of the mouse'''
		pass

	@property
	def map(self) -> Map:
		''' Currently played map'''
		pass

	@map.setter
	def map(self, value):
		''' Currently played map'''
		pass

	@property
	def keybinds(self) -> Keybind:
		''' Keybinds for casting spells/items etc'''
		pass

	@keybinds.setter
	def keybinds(self, value):
		''' Keybinds for casting spells/items etc'''
		pass

	@property
	def hud(self) -> GameHud:
		''' Gets the game HUD'''
		pass

	@hud.setter
	def hud(self, value):
		''' Gets the game HUD'''
		pass

	@property
	def hovered(self) -> Obj:
		''' Gets the game object under the mouse'''
		pass

	@hovered.setter
	def hovered(self, value):
		''' Gets the game object under the mouse'''
		pass

	@property
	def focused(self) -> Obj:
		''' Gets the game object focused (the object that was last clicked). None if last click was not on a object'''
		pass

	@focused.setter
	def focused(self, value):
		''' Gets the game object focused (the object that was last clicked). None if last click was not on a object'''
		pass

	@property
	def player(self) -> ChampionObj:
		''' The champion used by the local player. In replays this will be a random champion'''
		pass

	@player.setter
	def player(self, value):
		''' The champion used by the local player. In replays this will be a random champion'''
		pass

	@property
	def champs(self) -> ObjectQuery:
		''' Returns champion query builder'''
		pass

	@champs.setter
	def champs(self, value):
		''' Returns champion query builder'''
		pass

	@property
	def turrets(self) -> ObjectQuery:
		''' Returns turrets query builder'''
		pass

	@turrets.setter
	def turrets(self, value):
		''' Returns turrets query builder'''
		pass

	@property
	def missiles(self) -> ObjectQuery:
		''' Returns missiles query builder'''
		pass

	@missiles.setter
	def missiles(self, value):
		''' Returns missiles query builder'''
		pass

	@property
	def minions(self) -> ObjectQuery:
		''' Returns minions query builder'''
		pass

	@minions.setter
	def minions(self, value):
		''' Returns minions query builder'''
		pass

	@property
	def jungle(self) -> ObjectQuery:
		''' Returns jungle monster query builder'''
		pass

	@jungle.setter
	def jungle(self, value):
		''' Returns jungle monster query builder'''
		pass

	@property
	def others(self) -> ObjectQuery:
		''' Returns other uncategorized objects query builder'''
		pass

	@others.setter
	def others(self, value):
		''' Returns other uncategorized objects query builder'''
		pass

	def obj_by_net_id(self, net_id: int) -> Obj:
		'''     Returns the objects with the specified network id or None'''
		pass

	def raycast(self, begin: Vec3, direction: Vec3, length: float, width: float, layers: RayLayer) -> RaycastResult:
		'''     Launches a ray that stops on the first object specified by RayLayer'''
		pass

	def raycast(self, begin: Vec3, direction: Vec3, length: float, width: float, layers: RayLayer) -> RaycastResult:
		'''     Same as Context.Raycast but returns a list with all collision instead of the first collision.'''
		pass

	def is_wall_at(self, position: Vec3) -> bool:
		'''    Checks if there is a wall at the specified position'''
		pass

	def collisions_for(unit: UnitObj)-> list[FutureCollision]:
		'''    Gets a list of future collisions for a unit'''
		pass

	def collisions_for_unit(unit: UnitObj)-> list[FutureCollision]:
		'''    Gets a list of future collisions for a unit'''
		pass

	def collisions_for_spell(spell: SpellCast)-> list[FutureCollision]:
		'''    Gets a list of future collisions for a spell cast'''
		pass

	def attack(self, target: UnitObj):
		'''    Makes the player attack the given unit'''
		pass

	def move(self, location: Vec3):
		'''    Moves the player to the given location'''
		pass

	def move_to_location(self, location: Vec3):
		'''    Moves the player to where the mouse cursor is'''
		pass

	def move_to_mouse(self):
		'''    Moves the player to where the mouse cursor is'''
		pass

	def move_mouse(self, location: Vec3):
		'''    Moves the mouse location to the specified game world coordinate'''
		pass

	def is_held(self, key: Key) -> bool:
		'''    Checks if key is held down'''
		pass

	def was_pressed(self, key: Key) -> bool:
		'''    Checks if key was pressed'''
		pass

	def set_key_active(self, key: Key, active: bool):
		'''    Programatically disable/enable game keys. This means nothing will happen in game when the key gets pressed but valkyrie will still recognize that key. Use ctx.keybinds to get keys'''
		pass

	def start_channel(self, spell: SpellObj) -> bool:
		'''    Starts a channeled spell'''
		pass

	def end_channel(self, spell: SpellObj, location: Vec3) -> bool:
		'''    Ends and casts the channeled spell at the target location'''
		pass

	def cast_spell(self, spell: SpellObj, location: Vec3) -> bool:
		'''    Casts a spell on a location. If second argument is None, it will cast at the current mouse position. This function will check if spell is castable automatically. It doesnt check for item charge availability.'''
		pass

	def cast_spell_on_unit(self, spell: SpellObj, target: UnitObj) -> bool:
		'''    Casts a spell on a unit using prediction. If spell cannot be cast for some reason (no mana, unable to hit target etc) it will return False'''
		pass

	def predict_cast_point(self, caster: UnitObj, target: UnitObj, spell: SpellObj) -> Vec3:
		'''    Predicts a cast point such that the spell will hit the target. Returns None if doesnt find such a point'''
		pass

	def get_spell_static(self, spell_name: str) -> SpellStatic:
		'''    Gets static spell info. Argument must be lower case'''
		pass

	def is_under_tower(self, obj: Obj) -> bool:
		'''    True if the game object is under tower'''
		pass

	def is_at_spawn(self, obj: Obj) -> bool:
		'''    Checks if the object is in the fountain of his team'''
		pass

	def is_on_screen(self, point: Vec2) -> bool:
		'''    True if point is on screen'''
		pass

	def is_scren_point_on_screen(self, point: Vec2) -> bool:
		'''    True if point is on screen'''
		pass

	def is_world_point_on_screen(self, point: Vec3) -> bool:
		'''    True if point is on screen'''
		pass

	def w2s(self, position: Vec3) -> Vec2:
		'''    Converts a world space point to screen space'''
		pass

	def w2m(self, position: Vec3) -> Vec2:
		'''    Converts a world space point to minimap space'''
		pass

	def d2m(self, distance: float) -> float:
		'''    Converts a distance value from world space to minimap space'''
		pass

	def ping_normal(self, location: Vec3):
		'''    Issues a `normal` ping at the target location. For this ping type riot moves the cursor position to the ping location after ping has been issued'''
		pass

	def ping_warn(self, location: Vec3):
		'''    Issues a `back` ping at the target location. For this ping type riot moves the cursor position to the ping location after ping has been issued'''
		pass

	def ping_danger(self, location: Vec3):
		'''    Issues a `danger` ping at the target location'''
		pass

	def ping_mia(self, location: Vec3):
		'''    Issues a `enemy missing` ping at the target location'''
		pass

	def ping_omw(self, location: Vec3):
		'''    Issues a `on my way` ping at the target location'''
		pass

	def ping_vision(self, location: Vec3):
		'''    Issues a `warded` ping at the target location'''
		pass

	def ping_assist(self, location: Vec3):
		'''    Issues a `help` ping at the target location'''
		pass

	def hp_dmg_indicator(self, champ: ChampionObj, dmg: float, color: Col):
		'''     Draws an damage indicator with a specified color for an amount of damage on a champion hp bar.'''
		pass

	def line(self, start: Vec2, end: Vec2, thickness: float, color: Col):
		'''    '''
		pass

	def circle(self, center: Vec2, radius: float, num_pts: int, thickness: float, color: Col):
		'''    '''
		pass

	def circle_fill(self, center: Vec2, radius: float, num_pts: int, color: Col):
		'''    '''
		pass

	def text(self, position: Vec2, text: str, color: Col):
		'''    '''
		pass

	def rect(self, start: Vec2, size: Vec2, color: Col, rounding: float, thickness: float):
		'''    '''
		pass

	def rect_fill(self, start: Vec2, size: Vec2, color: Col, rounding: float):
		'''    '''
		pass

	def triangle(self, p1: Vec3, p2: Vec3, p3: Vec3, thickness: float, color: Col):
		'''    '''
		pass

	def triangle_fill(self, p1: Vec3, p2: Vec3, p3: Vec3, color: Col):
		'''    '''
		pass

	def image(self, id: str, position: Vec2, size: Vec2, color: Col):
		'''    '''
		pass

	def circle_world(self, center: Vec3, radius: float, num_pts: int, thickness: float, color: Col):
		'''    '''
		pass

	def circle_world_fill(self, center: Vec3, radius: float, num_pts: int, color: Col):
		'''    '''
		pass

	def rect_world(self, p1: Vec3, p2: Vec3, p3: Vec3, p4: Vec3, thickness: float, color: Col):
		'''    '''
		pass

	def image_uvs(self, id: str, position: Vec2, uv1: Vec2, uv2: Vec2, size: Vec2, color: Col):
		'''    '''
		pass

	def image_rounded(self, id: str, position: Vec2, size: Vec2, color: Col, rounding: float):
		'''    '''
		pass

	def image_world(self, id: str, position: Vec3, size: Vec2, color: Col):
		'''    '''
		pass

	def image_world_fixed(self, id: str, p1: Vec3, p2: Vec3, p3: Vec3, p4: Vec4, color: Col):
		'''    '''
		pass

	def pill(self, text: str, color_text: Col, color_background: Col):
		'''     Draws a pill with a text under the player. Pill positions are automatically managed each frame so that they dont overlap.'''
		pass

