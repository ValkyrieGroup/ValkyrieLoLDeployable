from valkyrie import *

key_blue = Key.t
key_red  = Key.w
key_gold = Key.e
look_for_card = None

def valkyrie_menu(ctx: Context):
	global key_blue, key_red, key_gold
	ui = ctx.ui

	key_blue = ui.keyselect('Key blue card', key_blue)
	key_red  = ui.keyselect('Key red card', key_red)
	key_gold = ui.keyselect('Key gold card', key_gold)


def valkyrie_on_load(ctx: Context):
	global key_blue, key_red, key_gold
	cfg = ctx.cfg

	key_blue = cfg.get_int('key_blue', key_blue)
	key_red  = cfg.get_int('key_red', key_red)
	key_gold = cfg.get_int('key_gold', key_gold)

def valkyrie_on_save(ctx: Context):
	cfg = ctx.cfg

	cfg.set_int('key_blue', key_blue)
	cfg.set_int('key_red', key_red)
	cfg.set_int('key_gold', key_gold)

def check_key(ctx, W, key, card_name):
	global look_for_card

	if ctx.was_pressed(key):
		look_for_card = card_name
		if key != Key.w and W.name == 'pickacard':
			ctx.cast_spell(W, None)

def valkyrie_exec(ctx: Context):
	global look_for_card

	W = ctx.player.W
	if not ctx.player.can_cast_spell(W):
		return

	check_key(ctx, W, key_blue, 'bluecardlock')
	check_key(ctx, W, key_red,  'redcardlock')
	check_key(ctx, W, key_gold, 'goldcardlock')

	if W.name == look_for_card:
		ctx.cast_spell(W, None)
		look_for_card = None