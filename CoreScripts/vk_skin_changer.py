from valkyrie import *			
from os import getenv 
import json

champ_skins           = None	
champ_skin_names      = None

champ_selected_skin   = 0
champ_selected_chroma = -1
champ_skin_id         = -1	

	
def valkyrie_menu(ctx: Context) :		 
	global champ_selected_skin, champ_selected_chroma, champ_skin_id
	ui = ctx.ui					 
	
	ui.text('Champion Skin')
	champ_selected_skin = ui.combo('Skin', champ_skin_names, champ_selected_skin)
	
	chromas = champ_skins[champ_selected_skin]['chromas']
	if len(chromas) > 0:
		ui.text('Skin Chromas')
		for i, chroma in enumerate(chromas):
			ui.pushid(id(chroma))
			if ui.button('', chroma['color']):
				champ_selected_chroma = i
			ui.popid()
			ui.sameline()
		ui.text('')
	else:
		champ_selected_chroma = -1
		
	ui.separator()
		
	if champ_selected_chroma != -1:
		champ_skin_id = chromas[champ_selected_chroma]['id']
	else:
		champ_skin_id = champ_skins[champ_selected_skin]['id']
		
	
def valkyrie_on_load(ctx: Context) :
	global champ_skins, champ_skin_names
	global champ_selected_skin, champ_selected_chroma, champ_skin_id

	cfg = ctx.cfg						 

	with open(getenv('APPDATA') + '\\Valkyrie\\data\\SkinInfo.json') as f:
		skins = json.loads(f.read())
		champ_skins = skins[ctx.player.name]
		champ_skin_names = [s['name'] for s in champ_skins]
		
		for skin in champ_skins:
			for chroma in skin['chromas']:
				color = chroma['color']
				chroma['color'] = Col(float((color >> 16) & 255) / 255.0, float((color >> 8) & 255) / 255.0, float(color & 255) / 255.0, 1.0)
	
	champ = ctx.player.name
	champ_selected_skin   = cfg.get_int(champ + '_champ_selected_skin'  , champ_selected_skin)
	champ_selected_chroma = cfg.get_int(champ + '_champ_selected_chroma', champ_selected_chroma)
	champ_skin_id         = cfg.get_int(champ + '_champ_skin_id'        , champ_skin_id) 

			
def valkyrie_on_save(ctx: Context) :	 
	cfg = ctx.cfg				 
	
	champ = ctx.player.name
	cfg.set_int(champ + '_champ_selected_skin'  , champ_selected_skin)
	cfg.set_int(champ + '_champ_selected_chroma', champ_selected_chroma)
	cfg.set_int(champ + '_champ_skin_id'        , champ_skin_id)   
								 
def valkyrie_exec(ctx: Context) :	     
	
	if not ctx.resources_loaded:
		return
	
	if champ_skin_id > -1:
		ctx.player.reskin(champ_skin_id)
