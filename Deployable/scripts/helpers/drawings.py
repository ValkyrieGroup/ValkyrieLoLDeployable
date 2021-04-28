from valkyrie import *
import json

class Circle:
	
	radius  = 0.0
	num_pts = 4
	width   = 1.0
	color   = Col.White
	filled  = False
	enabled = True
	
	mode_names = ['Primitive (laggier)', 'Rito Style']

	def __init__(self, rad, pts, width, col, fill, enabled, mode = 1):
		self.radius  = rad
		self.num_pts = pts
		self.width   = width
		self.color   = col
		self.filled  = fill
		self.enabled = enabled
		
		self.mode = mode
	
	def ui(self, label, ctx, fixed_radius = True):
		ui = ctx.ui
		
		ui.image('menu-circle', Vec2(15, 15), self.color)
		ui.sameline()
		if ui.beginmenu(label):
			self.mode    = ui.combo("Type", self.mode_names, self.mode)
			self.enabled = ui.checkbox("Enabled", self.enabled)
			self.filled  = ui.checkbox("Filled", self.filled)
			if not fixed_radius:
				self.radius = ui.dragfloat("Radius", self.radius)
			
			if self.mode == 0:
				self.width = ui.sliderfloat('Width', self.width, 1.0, 50.0)
				self.num_pts = ui.sliderint('Num points', self.num_pts, 4, 100)
			
			self.color = ui.colorpick("Color", self.color)
			ui.endmenu()
		

	def draw_at(self, ctx, pos):
		if self.enabled:
			if self.mode == 0:
				if self.filled:
					ctx.circle_fill(pos, self.radius, self.num_pts, self.color)
				else:
					ctx.circle(pos, self.radius, self.num_pts, self.width, self.color)
			else:
				ctx.image('circle1' if self.filled else 'circle1_nofill', pos, Vec2(self.radius*2.0, self.radius*2.0), self.color)
	
	@classmethod
	def from_str(self, serializable):
		serializable = json.loads(serializable)
		return Circle(serializable[0], serializable[1], serializable[2], Col(*(serializable[3])), serializable[4], serializable[5], serializable[6] if len(serializable) > 6 else 1)
	
	def __str__(self):
		return json.dumps([self.radius, self.num_pts, self.width, [self.color.r, self.color.g, self.color.b, self.color.a], self.filled, self.enabled, self.mode])
		
class Line:
	
	thickness = 2.0
	color     = Col.White
	enabled   = True
	
	def __init__(self, color, thickness, enabled):
		self.thickness = thickness
		self.enabled = enabled
		self.color = color
		
	def ui(self, label, ctx):
		ui = ctx.ui
		
		ui.image('menu-line', Vec2(15, 15), self.color)
		ui.sameline()
		if ui.beginmenu(label):
			self.enabled = ui.checkbox("Enabled", self.enabled)
			self.thickness = ui.sliderfloat("Thickness", self.thickness, 1.0, 5.0)
			self.color = ui.colorpick("Color", self.color)
			ui.endmenu()
		
	def draw_at(self, ctx, pos1, pos2):
		if self.enabled:
			ctx.line(pos1, pos2, self.thickness, self.color)
	
	@classmethod
	def from_str(self, serializable):
		serializable = json.loads(serializable)
		return Line(Col(*serializable[0]), serializable[1], serializable[2])
		
	def __str__(self):
		return json.dumps([[self.color.r, self.color.g, self.color.b, self.color.a], self.thickness, self.enabled])
		
class Image:

	color    = Col.White
	enabled  = True
	rounding = 0.0
	size     = 10.0
		
	def __init__(self, color, rounding, size, enabled):
		self.rounding = rounding
		self.enabled  = enabled
		self.size     = size
		self.color    = color
		
	def ui(self, label, ctx):
		ui = ctx.ui
		
		ui.image('garen_square', Vec2(15, 15), self.color)
		ui.sameline()
		if ui.beginmenu(label):
			self.enabled  = ui.checkbox("Enabled",     self.enabled)
			self.rounding = ui.sliderfloat("Rounding", self.rounding, 0.0, 15.0)
			self.size     = ui.sliderfloat("Size",     self.size, 10.0, 100.0)
			self.color    = ui.colorpick("Color mask", self.color)
			ui.endmenu()
		
	def draw_at(self, ctx, name, pos):
		if self.enabled:
			ctx.image(name, pos, Vec2(self.size, self.size), self.color, self.rounding)
	
	@classmethod
	def from_str(self, serializable):
		serializable = json.loads(serializable)
		return Image(Col(*serializable[0]), serializable[1], serializable[2], serializable[3])
		
	def __str__(self):
		return json.dumps([[self.color.r, self.color.g, self.color.b, self.color.a], self.rounding, self.size, self.enabled])
		
def draw_spell_track(ctx, spell, pos, size, rounding):

	cd = spell.cd
	color = Col.White
	if spell.lvl == 0:
		color = Col.Gray
	if cd > 0.0:
		color = Col.Red
		
	ctx.image(spell.static.icon if spell.static else 'none', pos, Vec2(size, size), color, rounding)
	if cd > 0.0 and size > 20:
		ctx.text(pos, str(int(cd)), Col.White)