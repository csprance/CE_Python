cvar = general.get_cvar('e_DebugDraw')

if cvar != 22:
	general.set_cvar('e_DebugDraw', 22)

if cvar == '22':
	general.set_cvar('e_DebugDraw', 0)
