# This is the CryPy utils module
# just contains a whole bunch of random helpful functions

import math

def cry_ruler(selection):
	'''utils.cry_ruler(tuple (firstObject, secondObject))'''
	if len(selection) > 2:
		general.message_box_ok('More then 2 Objects Selected')
	else:
		general.message_box_ok( str(fn_distance(selection[0], selection[1])))


# Calculate Distance between two points positions using Pythagoras Theorem
def fn_distance(pos1, pos2):
	distX = pos1[0] - pos2[0]
	distY = pos1[1] - pos2[1]
	distZ = pos1[2] - pos2[2]
	return math.sqrt(distX**2 + distY**2 + distZ**2)


	def main():
		cry_ruler(general.get_names_of_selected_objects())