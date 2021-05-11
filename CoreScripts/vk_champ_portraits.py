from valkyrie import *			 
							
portrait_size  = 80.0 
offsetX        = 0.65
offsetY        = -0.3

portrait_hsize  = None
portrait_vsize  = None
champ_icon_size = None
spell1_offset   = None
spell1_size     = None
spell2_offset   = None
spell2_size     = None

hpbar_size      = None
hpbar_offset    = None

def update_ratios():
	global portrait_hsize
	global portrait_vsize
	global champ_icon_size
	global spell1_offset  
	global spell1_size    
	global spell2_offset  
	global spell2_size 
	global hpbar_size  	
	global hpbar_offset	
	
	portrait_hsize  = portrait_size / 2.0
	portrait_vsize  = Vec2(portrait_size, portrait_size)		
	champ_icon_size = Vec2(portrait_size*0.75, portrait_size*0.75)
	spell1_offset   = Vec2(-portrait_size/5, portrait_size/3.2)
	spell1_size     = Vec2(portrait_size/4.0, portrait_size/4.0)
	spell2_offset   = Vec2(portrait_size/5.3, portrait_size/3.3)
	spell2_size     = Vec2(portrait_size/4.0, portrait_size/4.0)
	
	hpbar_size      = Vec2(50*(portrait_size*0.007), 122*(portrait_size*0.007))
	hpbar_offset    = Vec2(portrait_size*0.3, -portrait_size*0.05)
	
def valkyrie_menu(ctx: Context) :		 
	global portrait_size, offsetX, offsetY
	ui = ctx.ui	

	old_size = portrait_size
	portrait_size = ui.sliderfloat('Size portrait', portrait_size, 50.0, 200.0)
	offsetX       = ui.sliderfloat('Offset X', offsetX, -3.0, 3.0)
	offsetY       = ui.sliderfloat('Offset Y', offsetY, -3.0, 3.0)
	
	update_ratios()

def valkyrie_on_load(ctx: Context):
	global portrait_size
	global offsetX      
	global offsetY      
	cfg = ctx.cfg				 
	
	portrait_size = cfg.get_float('portrait_size', portrait_size)
	offsetX       = cfg.get_float('offsetX', offsetX)
	offsetY       = cfg.get_float('offsetY', offsetY)
	
	update_ratios()
	
def valkyrie_on_save(ctx: Context) :	 
	cfg = ctx.cfg				 
	
	cfg.set_float('portrait_size', portrait_size)
	cfg.set_float('offsetX', offsetX)
	cfg.set_float('offsetY', offsetY)

def draw_spell(ctx, spell, pos):
	cd = spell.cd
	ctx.image(spell.static.icon if spell.static else 'none',  pos, spell1_size, Col.White if cd == 0.0 else Col.Red, 15)
	if cd > 0.0:
		ctx.text(pos, str(int(cd)), Col.White)
	
def draw_portrait_for(ctx, champ, pos):
	
	p = max(0.25, champ.health/champ.max_health)
	hp_size = Vec2(hpbar_size.x, p*hpbar_size.y)
	hp_pos  = pos + Vec2(hpbar_offset.x, (1.0 -p)*portrait_size*0.4 + hpbar_offset.y)
	
	ctx.image("hud_champ_hpbar", hp_pos, hp_size, Vec2(0.0, 1.0 - p), Vec2(1.0, 1.0), Col.Green)
	
	ctx.image(champ.name + '_square', pos, champ_icon_size, Col.Red if champ.dead else (Col.White if champ.visible else Col.Gray), 100)
	ctx.image("hud_champ_portrait", pos, portrait_vsize, Col.White)
	miss_period = ctx.time - champ.last_seen
	if miss_period > 0.0:
		ctx.text(pos, str(int(miss_period)), Col.White)
	
	draw_spell(ctx, champ.spells[4], pos + spell1_offset)
	draw_spell(ctx, champ.spells[5], pos + spell2_offset)
				
def valkyrie_exec(ctx: Context) :	     
	
	hud = ctx.hud
	start_location = hud.minimap_pos.clone()
	start_location.x = hud.minimap_pos.x + hud.minimap_size.x*offsetX
	start_location.y = hud.minimap_pos.y + hud.minimap_size.y*offsetY
	
	for champ in ctx.champs.enemy_to(ctx.player).get():
		draw_portrait_for(ctx, champ, start_location)
		start_location.y -= portrait_size