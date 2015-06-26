cvar = general.get_cvar('p_draw_helpers')
print cvar

if cvar == '1':
	general.set_cvar('p_draw_helpers', '0')
else:
	general.set_cvar('p_draw_helpers', '1' )
