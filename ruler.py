# This is the CryPy utils module
# just contains a whole bunch of random helpful functions

import math


def cry_ruler(selection):
	"""utils.cry_ruler(tuple (firstObject, secondObject))"""
	if len(selection) > 2:
		general.message_box_ok('More then 2 Objects Selected')
	else:
		general.message_box_ok(str(fn_distance(general.get_position(selection[0]), general.get_position(selection[1]))))


def fn_distance(pos1, pos2):
	"""
	Calculate Distance between two points positions using Pythagoras Theorem
	@pos1: (x,y,z) - tuple3 of x,y,z position
	@pos2: (x,y,z) - tuple3 of x,y,z position
	"""
	dist__x = pos1[0] - pos2[0]
	dist__y = pos1[1] - pos2[1]
	dist__z = pos1[2] - pos2[2]
	return math.sqrt(dist__x ** 2 + dist__y ** 2 + dist__z ** 2)


if __name__ == '__main__':
	cry_ruler(general.get_names_of_selected_objects())
