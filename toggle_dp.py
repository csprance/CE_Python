cvar = general.get_cvar('r_Stats')

if cvar != 6:
	general.set_cvar('r_Stats', 6)

if cvar == '6':
	general.set_cvar('r_Stats', 0)